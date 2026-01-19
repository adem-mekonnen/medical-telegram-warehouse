# Medical Data Warehouse

A robust data engineering pipeline that extracts data from Ethiopian medical Telegram channels, stores it in a PostgreSQL warehouse, and transforms it using dbt for analytics.

## Project Structure
- `src/`: Python scripts for extraction (scraping), loading, and transformation.
- `medical_warehouse/`: dbt project containing data models (staging & marts).
- `scripts/`: Helper scripts.
- `tests/`: Unit tests.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd medical-telegram-warehouse