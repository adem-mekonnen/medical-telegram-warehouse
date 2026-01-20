from dagster import job, op, ScheduleDefinition, In, Nothing
import subprocess
import os
import sys

# Get the absolute path of the project root
PROJECT_ROOT = os.getcwd()
PYTHON_EXE = sys.executable 

@op
def scrape_telegram_data():
    """Step 1: Run the scraper"""
    print("🚀 Starting Scraper...")
    subprocess.run([PYTHON_EXE, "src/telegram.py", "--limit", "30"], check=True, cwd=PROJECT_ROOT)

# NOTICE: We removed 'start_after' from the function brackets below
@op(ins={"start_after": In(Nothing)})
def load_raw_to_postgres():
    """Step 2: Load JSON to Database"""
    print("📦 Loading Data...")
    subprocess.run([PYTHON_EXE, "src/loader.py"], check=True, cwd=PROJECT_ROOT)

@op(ins={"start_after": In(Nothing)})
def run_yolo_enrichment():
    """Step 3: Run AI Detection"""
    print("🤖 Running YOLO AI...")
    subprocess.run([PYTHON_EXE, "src/yolo_detect.py"], check=True, cwd=PROJECT_ROOT)

@op(ins={"start_after": In(Nothing)})
def run_dbt_transformations():
    """Step 4: Run dbt models and tests"""
    print("🏗️ Running dbt...")
    dbt_dir = os.path.join(PROJECT_ROOT, "medical_warehouse")
    
    # Run dbt run
    subprocess.run(["dbt", "run"], check=True, cwd=dbt_dir)
    
    # Run dbt test
    subprocess.run(["dbt", "test"], check=True, cwd=dbt_dir)

@job
def medical_pipeline_job():
    # Define the order of operations
    # We pass the output of the previous step to the 'start_after' argument of the next
    scraped = scrape_telegram_data()
    loaded = load_raw_to_postgres(start_after=scraped)
    enriched = run_yolo_enrichment(start_after=loaded)
    run_dbt_transformations(start_after=enriched)

# Define a schedule (Run once a day at midnight)
daily_schedule = ScheduleDefinition(job=medical_pipeline_job, cron_schedule="0 0 * * *")