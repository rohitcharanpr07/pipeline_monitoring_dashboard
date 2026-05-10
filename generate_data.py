import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --------------------------
# 1. PIPELINES MASTER TABLE
# --------------------------
pipelines = pd.DataFrame({
    "pipeline_id": [f"P{str(i).zfill(3)}" for i in range(1, 11)],
    "pipeline_name": [
        "Customer_ETL", "Order_Ingestion", "Finance_Load", "Inventory_Sync",
        "CRM_Update", "Billing_Transform", "Shipment_Tracking", "Sales_Aggregation",
        "HR_Data_Load", "Marketing_Analytics"
    ],
    "team": [
        "Sales", "Supply Chain", "Finance", "Operations",
        "CRM", "Finance", "Logistics", "Sales",
        "HR", "Marketing"
    ],
    "frequency": [
        "Daily", "Hourly", "Daily", "Every 6 hrs",
        "Hourly", "Daily", "Hourly", "Daily",
        "Daily", "Daily"
    ],
    "owner": [
        "Rohit", "Arjun", "Priya", "Kavin",
        "Anu", "Vikram", "John", "Sneha",
        "Divya", "Rahul"
    ]
})

pipelines.to_csv("pipelines.csv", index=False)

# --------------------------
# 2. PIPELINE RUNS
# --------------------------
runs = []

statuses = ["Success", "Failed", "Delayed", "Running"]
status_probs = [0.75, 0.10, 0.10, 0.05]

start_date = datetime(2025, 1, 1)

for i in range(1, 1001):
    pipeline_id = random.choice(pipelines["pipeline_id"].tolist())
    run_date = start_date + timedelta(days=random.randint(0, 120))
    start_time = run_date + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
    
    status = np.random.choice(statuses, p=status_probs)

    runtime = random.randint(10, 90)
    if status == "Failed":
        runtime = random.randint(5, 30)
    elif status == "Delayed":
        runtime = random.randint(60, 180)

    end_time = start_time + timedelta(minutes=runtime)

    records_processed = random.randint(50000, 10000000) if status != "Failed" else 0
    compute_cost = round(runtime * random.uniform(0.05, 0.5), 2)

    runs.append([
        f"R{str(i).zfill(4)}",
        pipeline_id,
        run_date.date(),
        start_time,
        end_time,
        status,
        records_processed,
        compute_cost
    ])

pipeline_runs = pd.DataFrame(runs, columns=[
    "run_id", "pipeline_id", "run_date", "start_time",
    "end_time", "status", "records_processed", "compute_cost"
])

pipeline_runs.to_csv("pipeline_runs.csv", index=False)

# --------------------------
# 3. SLA TRACKING
# --------------------------
sla_tracking = []

for _, row in pipeline_runs.iterrows():
    actual_runtime = int((pd.to_datetime(row["end_time"]) - pd.to_datetime(row["start_time"])).total_seconds() / 60)
    sla_target = random.choice([30, 45, 60, 90])
    sla_breached = "Yes" if actual_runtime > sla_target else "No"

    sla_tracking.append([
        row["run_id"],
        sla_target,
        actual_runtime,
        sla_breached
    ])

sla_df = pd.DataFrame(sla_tracking, columns=[
    "run_id", "sla_target_mins", "actual_runtime_mins", "sla_breached"
])

sla_df.to_csv("sla_tracking.csv", index=False)

# --------------------------
# 4. INCIDENTS
# --------------------------
incident_types = ["Config Error", "Query Error", "Infra Failure", "Timeout", "Schema Mismatch", "Network Failure"]
severity_levels = ["Low", "Medium", "High", "Critical"]

incidents = []

failed_runs = pipeline_runs[pipeline_runs["status"].isin(["Failed", "Delayed"])]

for i, (_, row) in enumerate(failed_runs.iterrows(), start=1):
    incidents.append([
        f"I{str(i).zfill(4)}",
        row["run_id"],
        random.choice(incident_types),
        random.choice(severity_levels),
        random.randint(10, 180)
    ])

incidents_df = pd.DataFrame(incidents, columns=[
    "incident_id", "run_id", "issue_type", "severity", "resolved_time_mins"
])

incidents_df.to_csv("incidents.csv", index=False)
