import os
import sqlite3
import json
import urllib.request
import time

PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID", "rapmepbfhsygjadsretx")
TOKEN = os.getenv("SUPABASE_ACCESS_TOKEN", "")
API_URL = f"https://api.supabase.com/v1/projects/{PROJECT_ID}/database/query"

conn = sqlite3.connect("d:/Tech Pulse AI/techpulse.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def run_supabase_sql(query):
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"query": query}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as res:
                return json.loads(res.read().decode("utf-8"))
        except Exception as e:
            if attempt == 2:
                raise e
            time.sleep(2)

def sql_quote(val, col_name, bool_cols, json_cols):
    if val is None:
        return "NULL"
    if col_name in bool_cols:
        return "TRUE" if val in (1, True, "1", "true", "True") else "FALSE"
    if col_name in json_cols:
        if isinstance(val, (dict, list)):
            s = json.dumps(val).replace("'", "''")
        else:
            s = str(val).replace("'", "''")
        return f"'{s}'::jsonb"
    if isinstance(val, (int, float)):
        return str(val)
    s = str(val).replace("'", "''")
    return f"'{s}'"

def migrate_table(table, columns, conflict_col, bool_cols, json_cols, batch_size=50):
    cols_str = ", ".join(columns)
    cur.execute(f"SELECT {cols_str} FROM {table}")
    rows = cur.fetchall()
    total = len(rows)
    print(f"\n--- Migrating {table} ({total} rows) ---")

    for i in range(0, total, batch_size):
        batch = rows[i:i+batch_size]
        vals = []
        for r in batch:
            row_vals = [sql_quote(r[col], col, bool_cols, json_cols) for col in columns]
            vals.append(f"({', '.join(row_vals)})")
        sql = f"INSERT INTO public.{table} ({cols_str}) VALUES\n" + ",\n".join(vals) + f"\nON CONFLICT ({conflict_col}) DO NOTHING;"
        run_supabase_sql(sql)
        print(f"  Inserted rows {i+1} to {min(i+batch_size, total)} of {total}")

print("Starting Supabase Migration for TechPulse AI...")

# 1. items (parent table)
migrate_table(
    "items",
    ["id", "source", "source_id", "title", "description", "url", "metadata_json", "ingested_at", "created_at"],
    "id",
    set(),
    {"metadata_json"},
    50
)

# 2. classifications (depends on items)
migrate_table(
    "classifications",
    ["id", "item_id", "primary_domain", "secondary_domains", "confidence_scores", "low_confidence", "model_version", "classified_at"],
    "id",
    {"low_confidence"},
    {"secondary_domains", "confidence_scores"},
    100
)

# 3. predictions (depends on items)
migrate_table(
    "predictions",
    ["id", "item_id", "prediction_type", "score", "score_display", "confidence", "features_used", "model_version", "predicted_at"],
    "id",
    set(),
    {"features_used"},
    100
)

# 4. insights (depends on items)
migrate_table(
    "insights",
    ["id", "item_id", "summary", "key_takeaways", "why_it_matters", "technical_depth", "estimated_read_time", "related_topics", "llm_model", "generated_at"],
    "id",
    set(),
    {"key_takeaways", "related_topics"},
    50
)

# 5. domain_trends
migrate_table(
    "domain_trends",
    ["id", "domain", "date", "item_count", "avg_impact", "trend_score", "wow_delta", "is_trending", "hype_adoption_ratio", "aggregated_at"],
    "id",
    {"is_trending"},
    set(),
    100
)

# 6. pipeline_errors
migrate_table(
    "pipeline_errors",
    ["id", "task_name", "item_id", "error_msg", "occurred_at"],
    "id",
    set(),
    set(),
    100
)

print("\n--- Migration Complete! Verifying row counts on Supabase ---")
tables = ["items", "classifications", "predictions", "insights", "domain_trends", "pipeline_errors"]
for t in tables:
    res = run_supabase_sql(f"SELECT count(*) FROM public.{t};")
    count = res[0]["count"] if res else 0
    print(f"Supabase public.{t}: {count} rows")
