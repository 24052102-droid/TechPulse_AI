# TechPulse AI — Deployment Guide

> **Stack:** FastAPI backend on **Render.com** · React frontend on **Vercel** · Daily data refresh via **GitHub Actions**

---

## Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│  GitHub Actions                                              │
│  ├── keep-warm.yml    → pings /api/health every 10 min      │
│  └── daily-ingest.yml → POST /api/admin/refresh at 00:05 UTC│
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP POST
              ┌────────────▼────────────┐
              │  Render.com (free tier) │
              │  FastAPI + Uvicorn      │
              │  /api/admin/refresh     │──► arXiv API
              │  triggers 6-stage       │──► GitHub API
              │  pipeline               │──► HN Firebase API
              └────────────┬────────────┘
                           │ SQL
              ┌────────────▼────────────┐
              │  Supabase PostgreSQL 15 │  (free tier)
              └─────────────────────────┘

              ┌─────────────────────────┐
              │  Vercel (free tier)     │
              │  React / Vite frontend  │──► calls Render /api/*
              └─────────────────────────┘
```

---

## Step 1 — Set Up Supabase Database (Required)

1. Go to [supabase.com](https://supabase.com) → **New Project**
2. Note your **Project URL** and **Database Password**
3. Copy the **Transaction Pooler** connection string (port 6543):
   ```
   postgresql://postgres.XXXX:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
   ```
4. You'll use this as `DATABASE_URL` in Step 2.

> **Note:** The free Supabase plan gives you 500 MB storage and 2 CPU cores — more than enough.

---

## Step 2 — Deploy Backend on Render

### 2a. Connect your GitHub repo
1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect your GitHub repo (`TechPulse-AI`)
3. Render will auto-detect `render.yaml` — click **Apply**

### 2b. Set environment variables in Render Dashboard

Go to your `techpulse-backend` service → **Environment** tab and add:

| Variable | Value | Required? |
|----------|-------|-----------|
| `DATABASE_URL` | Supabase PostgreSQL URL (port 6543) | ✅ Required |
| `GROQ_API_KEY` | Your Groq API key from [console.groq.com](https://console.groq.com) | ✅ Required for AI summaries |
| `GITHUB_PAT` | GitHub Personal Access Token (no scopes needed, just for higher rate limits) | ⚠️ Recommended |
| `REDIS_URL` | Upstash Redis URL (optional — in-memory cache used as fallback) | Optional |

> **Free API Keys:**
> - **Groq** — free at [console.groq.com](https://console.groq.com), 30 req/min on free tier
> - **GitHub PAT** — free at [github.com/settings/tokens](https://github.com/settings/tokens), select "No scopes"
> - **Upstash Redis** — free at [upstash.com](https://upstash.com), 10,000 req/day free

### 2c. Note your Render service URL

After deploy, your backend will be live at something like:
```
https://techpulse-backend.onrender.com
```
Copy the exact URL from the Render dashboard.

---

## Step 3 — Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com) → **New Project** → import `TechPulse-AI`
2. Vercel will detect `vercel.json` automatically
3. In **Environment Variables**, add:

   | Variable | Value |
   |----------|-------|
   | `VITE_API_BASE_URL` | `https://techpulse-backend.onrender.com` |

4. Click **Deploy** — your frontend will be live at `https://techpulse-ai.vercel.app`

5. **Update CORS in Render**: Go back to your Render service → Environment, update:
   ```
   CORS_ORIGINS=["https://techpulse-ai.vercel.app","http://localhost:5173"]
   ```

---

## Step 4 — Configure GitHub Actions Secrets

In your GitHub repo → **Settings** → **Secrets and variables** → **Actions**, add:

| Secret | Value |
|--------|-------|
| `RENDER_BACKEND_URL` | `https://techpulse-backend.onrender.com` |

This enables both:
- **`keep-warm.yml`** — pings `/api/health` every 10 minutes (prevents Render free-tier sleep)
- **`daily-ingest.yml`** — triggers full data refresh from arXiv, GitHub & HN every day at 00:05 UTC

---

## Step 5 — Seed Initial Data

After the backend is live, trigger a first data load:

**Option A — Via the UI:**
Open the frontend → go to **Evaluation** page → click **"Trigger Refresh"**

**Option B — Via GitHub Actions:**
Go to repo → **Actions** → **Daily Data Refresh** → **Run workflow** (set `max_results=50`)

**Option C — Via curl:**
```bash
curl -X POST "https://techpulse-backend.onrender.com/api/admin/refresh?max_results=50"
```

---

## Daily Schedule (GitHub Actions)

| Workflow | Schedule | Action |
|----------|----------|--------|
| `keep-warm.yml` | Every 10 minutes | Pings `/api/health` to prevent Render sleep |
| `daily-ingest.yml` | Daily at 00:05 UTC (05:35 IST) | Runs 6-stage pipeline: arXiv + GitHub + HN ingest, classify, predict, insights |

---

## Required vs Optional Services

| Service | Required? | Free Tier? | Purpose |
|---------|-----------|------------|---------|
| Render (Web Service) | ✅ | ✅ 750 hrs/month | FastAPI backend |
| Supabase | ✅ | ✅ 500 MB | PostgreSQL database |
| Vercel | ✅ | ✅ Unlimited | React frontend |
| GitHub Actions | ✅ | ✅ 2000 min/month | Daily data refresh + keep-warm |
| Groq API | ✅ for AI cards | ✅ 30 req/min | LLM insight synthesis |
| GitHub PAT | ⚠️ Recommended | ✅ Free | Higher GitHub API rate limits |
| Upstash Redis | Optional | ✅ 10k req/day | Feed caching (in-memory fallback if absent) |
| Render Worker (Celery) | Optional | ❌ Paid | Alternative to GitHub Actions cron |

> **Minimum viable free stack:** Render + Supabase + Vercel + GitHub Actions + Groq

---

## Troubleshooting

### Backend returns 500 on startup
- Check `DATABASE_URL` is set and the Supabase project is active
- Check Render logs: Dashboard → your service → **Logs**

### Feed shows 0 items
- The database is empty — run an initial refresh (Step 5 above)

### CORS errors in browser
- Ensure `CORS_ORIGINS` in Render includes your exact Vercel URL (no trailing slash)

### GitHub Actions daily-ingest times out
- Render free tier may be sleeping — `keep-warm.yml` should prevent this, but if the workflow still fails, manually trigger it first to wake the instance

### arXiv/GitHub data not updating
- Check GitHub Actions → **Daily Data Refresh** logs
- Verify `RENDER_BACKEND_URL` secret is set in GitHub repo settings

---

## Local Development

```bash
# 1. Copy env file
cp .env.example .env
# Edit .env with your DATABASE_URL and GROQ_API_KEY

# 2. Install backend
pip install -r requirements.txt

# 3. Run FastAPI
uvicorn backend.app.main:app --reload

# 4. In a new terminal, run frontend
cd Frontend && npm install && npm run dev
```

The frontend dev server proxies `/api` to `http://127.0.0.1:8000` automatically.
