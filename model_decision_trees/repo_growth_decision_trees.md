# GitHub Repository Growth Model — Decision Tree Inspection

**Model Version:** `repo_growth_xgb_v1.0`  
**Algorithm:** Extreme Gradient Boosting (`XGBRegressor`)  
**Trained Date:** `2026-10-27T21:42:13.667809+00:00`  
**Hyperparameters:** 300 Trees · Max Depth 6 · Learning Rate $\eta = 0.05$ · Subsample 0.8 · ColSample 0.8  
**Validation Results:** 5-Fold CV RMSE = `0.0617 ± 0.0025` | Holdout Test RMSE = `0.0359` | $R^2 = 0.5259$

---

## 1. Feature Importance & Cumulative Split Gain (All 300 Trees)

| Feature | Total Splits Across 300 Trees | Total Cumulative Gain | Gain Share (%) | Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| `days_since_commit` | 2,228 | 462.27 | 41.6% | Commit recency & developer activity freshness (Highest weight) |
| `stars_log` | 2,717 | 389.65 | 35.1% | Initial star baseline volume log-transformed |
| `forks` | 1,834 | 73.55 | 6.6% | General repository metadata |
| `fork_star_ratio` | 2,147 | 52.56 | 4.7% | Forks per star (utility and developer contribution signal) |
| `readme_length` | 1,961 | 39.25 | 3.5% | Documentation quality & completeness |
| `open_issues` | 1,690 | 23.18 | 2.1% | Community usage and issue tracker velocity |
| `topic_count` | 1,127 | 22.27 | 2.0% | Tag specificity and ecosystem discoverability |
| `lang_other` | 236 | 11.59 | 1.0% | Implementation programming language |
| `lang_TypeScript` | 216 | 6.29 | 0.6% | Implementation programming language |
| `lic_MIT` | 241 | 4.27 | 0.4% | Open source license permissiveness |
| `lang_Python` | 210 | 4.16 | 0.4% | Implementation programming language |
| `lic_none` | 194 | 3.69 | 0.3% | Open source license permissiveness |
| `lic_other` | 182 | 3.25 | 0.3% | Open source license permissiveness |
| `lang_Rust` | 161 | 3.15 | 0.3% | Implementation programming language |
| `lang_JavaScript` | 161 | 3.07 | 0.3% | Implementation programming language |
| `lang_C++` | 106 | 2.79 | 0.3% | Implementation programming language |
| `lic_Apache-2.0` | 215 | 2.45 | 0.2% | Open source license permissiveness |
| `lang_Go` | 105 | 1.77 | 0.2% | Implementation programming language |
| `lic_GPL-3.0` | 58 | 0.92 | 0.1% | Open source license permissiveness |

---

## 2. Tree 0: The Baseline Star Velocity Tree

### Diagram: Tree 0 (Primary Splits)
```mermaid
graph TD
    N0["stars_log &lt; 9.613<br/><small>Gain: 32.44</small>"]:::decision
    N0 -->|Yes / True| N1
    N0 -->|No / False| N2
    N1["stars_log &lt; 7.296<br/><small>Gain: 5.39</small>"]:::decision
    N1 -->|Yes / True| N3
    N1 -->|No / False| N4
    N2["stars_log &lt; 10.334<br/><small>Gain: 3.84</small>"]:::decision
    N2 -->|Yes / True| N5
    N2 -->|No / False| N6
    N3["stars_log &lt; 6.332<br/><small>Gain: 0.57</small>"]:::decision
    N3 -->|Yes / True| N7
    N3 -->|No / False| N8
    N4["stars_log &lt; 8.925<br/><small>Gain: 1.39</small>"]:::decision
    N4 -->|Yes / True| N9
    N4 -->|No / False| N10
    N5["fork_star_ratio &lt; 0.142<br/><small>Gain: 0.87</small>"]:::decision
    N5 -->|Yes / True| N11
    N5 -->|No / False| N12
    N6["lang_other &lt; 1.0<br/><small>Gain: 1.06</small>"]:::decision
    N6 -->|Yes / True| N13
    N6 -->|No / False| N14
    N7["Subtree (lic_none split, gain=0.09)"]:::sub
    N8["Subtree (topic_count split, gain=0.29)"]:::sub
    N9["Subtree (lang_other split, gain=0.52)"]:::sub
    N10["Subtree (lang_other split, gain=0.53)"]:::sub
    N11["Subtree (lang_TypeScript split, gain=0.39)"]:::sub
    N12["Subtree (lang_other split, gain=0.22)"]:::sub
    N13["Subtree (stars_log split, gain=0.80)"]:::sub
    N14["Subtree (readme_length split, gain=0.66)"]:::sub
    classDef decision fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef leaf fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#ecfdf5;
    classDef sub fill:#312e81,stroke:#818cf8,stroke-width:1px,color:#e0e7ff;
```

### Detailed Decision Logic of Tree 0:
1. **Root Split (`stars_log < 9.613`):**
   * Corresponds to approx 14,950 stars.
   * Repositories with >= 15,000 existing stars follow a viral compounding trajectory where absolute 30-day star deltas are dramatically higher.
2. **Sub-Tier Split (`stars_log < 7.296` ~ 1,475 stars):**
   * Differentiates early-stage emerging repositories (<1,500 stars) from established mid-tier projects (1,500 - 15,000 stars).
3. **Utility Threshold (`fork_star_ratio < 0.1418`):**
   * Repositories where at least 14.2% of stargazers also fork the repo demonstrate high utility rather than passive bookmarking.

---

## 3. Tree 1: Commit Recency & Freshness Penalty

Tree 1 applies strict decay penalties for inactive repositories.

### Diagram: Tree 1
```mermaid
graph TD
    N0["days_since_commit &lt; 21.0<br/><small>Gain: 40.83</small>"]:::decision
    N0 -->|Yes / True| N1
    N0 -->|No / False| N2
    N1["stars_log &lt; 9.338<br/><small>Gain: 22.11</small>"]:::decision
    N1 -->|Yes / True| N3
    N1 -->|No / False| N4
    N2["days_since_commit &lt; 60.0<br/><small>Gain: 2.42</small>"]:::decision
    N2 -->|Yes / True| N5
    N2 -->|No / False| N6
    N3["stars_log &lt; 6.88<br/><small>Gain: 4.27</small>"]:::decision
    N3 -->|Yes / True| N7
    N3 -->|No / False| N8
    N4["stars_log &lt; 10.334<br/><small>Gain: 2.23</small>"]:::decision
    N4 -->|Yes / True| N9
    N4 -->|No / False| N10
    N5["stars_log &lt; 7.637<br/><small>Gain: 1.25</small>"]:::decision
    N5 -->|Yes / True| N11
    N5 -->|No / False| N12
    N6["days_since_commit &lt; 119.0<br/><small>Gain: 0.17</small>"]:::decision
    N6 -->|Yes / True| N13
    N6 -->|No / False| N14
    N7["Subtree (stars_log split, gain=0.45)"]:::sub
    N8["Subtree (stars_log split, gain=0.83)"]:::sub
    N9["Subtree (fork_star_ratio split, gain=0.28)"]:::sub
    N10["Subtree (stars_log split, gain=0.29)"]:::sub
    N11["Subtree (stars_log split, gain=0.08)"]:::sub
    N12["Subtree (stars_log split, gain=0.54)"]:::sub
    N13["Subtree (stars_log split, gain=0.16)"]:::sub
    N14["🍃 Leaf Output: -0.0039"]:::leaf
    classDef decision fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef leaf fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#ecfdf5;
    classDef sub fill:#312e81,stroke:#818cf8,stroke-width:1px,color:#e0e7ff;
```

### Key Insight from Tree 1:
* Regardless of star count, repositories with `days_since_commit >= 60` receive severe negative leaf penalties.
* Fresh repositories committed to within 7 days receive compounding positive velocity boosts.

---

## 4. Tree 2: Language & License Multipliers

### Diagram: Tree 2
```mermaid
graph TD
    N0["days_since_commit &lt; 29.0<br/><small>Gain: 37.56</small>"]:::decision
    N0 -->|Yes / True| N1
    N0 -->|No / False| N2
    N1["stars_log &lt; 9.305<br/><small>Gain: 22.36</small>"]:::decision
    N1 -->|Yes / True| N3
    N1 -->|No / False| N4
    N2["days_since_commit &lt; 62.0<br/><small>Gain: 1.19</small>"]:::decision
    N2 -->|Yes / True| N5
    N2 -->|No / False| N6
    N3["stars_log &lt; 6.88<br/><small>Gain: 4.08</small>"]:::decision
    N3 -->|Yes / True| N7
    N3 -->|No / False| N8
    N4["stars_log &lt; 10.632<br/><small>Gain: 2.2</small>"]:::decision
    N4 -->|Yes / True| N9
    N4 -->|No / False| N10
    N5["stars_log &lt; 9.731<br/><small>Gain: 0.73</small>"]:::decision
    N5 -->|Yes / True| N11
    N5 -->|No / False| N12
    N6["days_since_commit &lt; 112.0<br/><small>Gain: 0.12</small>"]:::decision
    N6 -->|Yes / True| N13
    N6 -->|No / False| N14
    N7["Subtree (stars_log split, gain=0.52)"]:::sub
    N8["Subtree (stars_log split, gain=0.82)"]:::sub
    N9["Subtree (stars_log split, gain=0.46)"]:::sub
    N10["Subtree (stars_log split, gain=0.23)"]:::sub
    N11["Subtree (stars_log split, gain=0.32)"]:::sub
    N12["Subtree (forks split, gain=0.05)"]:::sub
    N13["Subtree (stars_log split, gain=0.16)"]:::sub
    N14["Subtree (days_since_commit split, gain=0.00)"]:::sub
    classDef decision fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef leaf fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#ecfdf5;
    classDef sub fill:#312e81,stroke:#818cf8,stroke-width:1px,color:#e0e7ff;
```

---

## 5. End-to-End Prediction Walkthrough (How a Repo is Scored)

1. `FeatureExtractor` extracts the 20 numerical dimensions from the repository snapshot.
2. The item starts with base score ~0.080.
3. Traverses all 300 boosting trees, accumulating leaf weights.
4. Clamped to $[0.0, 1.0]$ and scaled to $0.0 - 10.0$ for the UI badge.
5. TreeSHAP determines the exact top 3 positive or negative drivers (e.g. `days_since_commit: -0.071 (105 days stale)`, `stars_log: +0.156`).
