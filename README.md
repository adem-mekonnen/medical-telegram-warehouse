# Medical Data Warehouse (End-to-End Data Pipeline)

**A robust data engineering pipeline** that extracts data from Ethiopian medical Telegram channels, validates and stores it in a PostgreSQL Data Warehouse, enriches it using Computer Vision (YOLOv8), exposes insights via a REST API, and orchestrates the entire workflow using Dagster.

## 📂 Project Structure

Based on the repository layout:

```text
medical-telegram-warehouse/
├── .github/                 # GitHub Actions/Workflows
├── api/                     # FastAPI application (Task 4)
│   ├── main.py              # API Endpoints
│   ├── database.py          # DB Connection
│   └── schemas.py           # Pydantic Models
├── data/                    # Data Lake (Raw JSON & Images)
├── logs/                    # Execution logs
├── medical_warehouse/       # dbt Project (Task 2)
│   ├── models/              # Staging & Marts (SQL transformations)
│   ├── tests/               # Data integrity tests
│   └── dbt_project.yml      # dbt configuration
├── src/                     # Core ETL Scripts
│   ├── telegram.py          # Task 1: Scraper
│   ├── loader.py            # Task 2: Data Loader
│   ├── yolo_detect.py       # Task 3: AI Enrichment
│   └── orchestrate.py       # Task 5: Dagster Pipeline
├── docker-compose.yml       # PostgreSQL Container Config
├── requirements.txt         # Python dependencies
└── README.md                # Project Documentation
```

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd medical-telegram-warehouse
```

### 2. Set Up Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named **`.env`** in the root directory and add your credentials:

```env
# Telegram API (from my.telegram.org)
Tg_API_ID=your_api_id
Tg_API_HASH=your_api_hash

# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=5455
DB_NAME=medical_warehouse
DB_USER=user
DB_PASSWORD=newpass123
```

### 5. Start the Database
```bash
docker-compose up -d
```

---

## 🚀 Running the Pipeline

You can run the pipeline manually step-by-step, or automatically using Dagster.

### Option A: Manual Execution (Step-by-Step)

**Task 1: Extract (Scraping)**
Scrapes Telegram channels and saves raw JSON/Images to `data/`.
```bash
python src/telegram.py --limit 50
```

**Task 2: Load & Transform (ELT)**
Loads raw JSON into PostgreSQL and transforms it into a Star Schema.
```bash
# Load to DB
python src/loader.py

# Transform with dbt
cd medical_warehouse
dbt run
dbt test
cd ..
```

**Task 3: Enrichment (AI Object Detection)**
Detects objects in downloaded images and classifies them (Promotional vs Product).
```bash
# Run YOLO analysis
python src/yolo_detect.py

# Update Warehouse tables
cd medical_warehouse
dbt run
cd ..
```

---

### Option B: Automated Orchestration (Dagster) 🌟

**Task 5:** Run the entire pipeline (Scrape -> Load -> Enrich -> Transform) with one click.

1.  **Start the Dagster UI:**
    ```bash
    dagster dev -f src/orchestrate.py
    ```
2.  Open **http://127.0.0.1:3000** in your browser.
3.  Go to **Jobs** > **medical_pipeline_job** > **Launchpad**.
4.  Click **Launch Run**.

---

## 📊 Analytical API (FastAPI)

**Task 4:** Serve the cleaned data to frontend applications.

1.  **Start the API Server:**
    ```bash
    uvicorn api.main:app --reload
    ```
2.  **Access Documentation:**
    Open **http://127.0.0.1:8000/docs** to test the endpoints interactively.

**Available Endpoints:**
*   `GET /api/reports/top-products`: Most frequently mentioned terms.
*   `GET /api/channels/{name}/activity`: Daily posting trends.
*   `GET /api/search/messages`: Full-text search.
*   `GET /api/reports/visual-content`: AI-based image classification stats.

---

## 🧪 Testing

To ensure data integrity, we use dbt tests.

```bash
cd medical_warehouse
dbt test
```
*   Checks for Unique IDs.
*   Ensures no NULL values in critical columns.
*   Validates logical consistency (e.g., no future dates).

---

## 🏗️ Architecture

1.  **Extract:** Python script uses `Telethon` to scrape Telegram.
2.  **Load:** Python script loads JSON to PostgreSQL (Raw Layer).
3.  **Enrich:** `YOLOv8` processes images to extract metadata.
4.  **Transform:** `dbt` models data into a Star Schema (`fct_messages`, `dim_dates`, `dim_channels`).
5.  **Serve:** `FastAPI` exposes the final tables via JSON REST endpoints.
6.  **Orchestrate:** `Dagster` manages dependencies and scheduling.
```