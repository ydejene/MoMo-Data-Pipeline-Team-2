# MoMo-Data-Pipeline-Team-2

## Team 2 - MoMo SMS ETL Project
### Team Members
- Brian
- Derick
- Habibllah
- Yonas

---

## Links
- **Architecture Diagram:** [Link to Architecture Diagram](./docs/architecture-diagram.png)
- **Scrum Board:** [Team 2 Scrum Board](https://alustudent-team-k1plq8kl.atlassian.net/jira/software/projects/T2MSEP/boards/34?jql=&atlOrigin=eyJpIjoiN2ZkZGMzNjFhMTZkNGQzODg4MTM1YzI2ZGIyZDZiODAiLCJwIjoiaiJ9)

---

## Project Overview
An enterprise-level fullstack application to process MoMo SMS data (XML), categorize transactions, and visualize insights via a dashboard.

---

## Table of Contents (more to be added as we build up)

- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)

---

## System Architecture

### High-Level Overview
Our system follows a layered architecture pattern with clear separation of concerns:
- **Data Ingestion** → **Processing** → **Storage** → **API/Export** → **Visualization**

[Link to Architecture Diagram](./docs/architecture-diagram.png)

### Architecture Components

#### 1️ Data Source Layer
| Component | Purpose | Technology |
|-----------|---------|------------|
| `momo.xml` | Raw MoMo SMS transaction data in XML format | XML |

#### 2️ ETL Pipeline (Backend Processing)
| Component | File | Purpose |
|-----------|------|---------|
| **XML Parser** | `etl/parse_xml.py` | Reads and validates XML structure, extracts transaction records |
| **Data Cleaner** | `etl/clean_normalize.py` | Normalizes amounts (removes currency symbols), standardizes date formats, normalizes phone numbers |
| **Categorizer** | `etl/categorize.py` | Applies business rules to classify transactions (e.g., airtime, transfer, bill payment) |
| **Error Handler** | Built into pipeline | Captures malformed/invalid data and routes to dead letter queue |
| **ETL Orchestrator** | `etl/run.py` | CLI tool that coordinates the entire ETL workflow |
| **Logger** | `data/logs/etl.log` | Records all ETL operations, errors, and audit trail for debugging and monitoring |

#### 3️ Storage Layer
| Component | File/Location | Purpose |
|-----------|---------------|---------|
| **SQLite Database** | `data/db.sqlite3` | Relational database storing normalized transaction data in structured tables |
| **Dashboard Cache** | `data/processed/dashboard.json` | Pre-aggregated analytics data for fast frontend loading without database queries |
| **Dead Letter Queue** | `data/logs/dead_letter/` | Stores unparsed or invalid XML snippets for manual review and data quality monitoring |

#### 4️ API Layer (Optional - Feature)
| Component | File | Purpose |
|-----------|------|---------|
| **FastAPI Backend** | `api/app.py` | RESTful API server providing programmatic access to transaction data |
| **Endpoints** | | • `GET /transactions` - Retrieve filtered transaction list<br>• `GET /analytics` - Get aggregated statistics<br>• `GET /categories` - List transaction categories |
| **Database Helper** | `api/db.py` | SQLite connection pool and query utilities |
| **Data Schemas** | `api/schemas.py` | Pydantic models for request/response validation |

#### 5️ Presentation Layer (Frontend)
| Component | File | Purpose |
|-----------|------|---------|
| **Dashboard UI** | `index.html` | Main user interface for viewing transactions and analytics |
| **Visualization Engine** | `web/chart_handler.js` | Fetches data and renders interactive charts and tables |
| **Styling** | `web/styles.css` | Responsive design and visual styling |
| **Assets** | `web/assets/` | Icons, images, and other static resources |

#### Automation Scripts
| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/run_etl.sh` | Executes the complete ETL pipeline from XML to database | `./scripts/run_etl.sh` |
| `scripts/export_json.sh` | Regenerates `dashboard.json` with latest aggregated data | `./scripts/export_json.sh` |
| `scripts/serve_frontend.sh` | Starts local development server for testing the dashboard | `./scripts/serve_frontend.sh` |

### Data Flow
```
1. XML File (momo.xml) 
   ↓
2. ETL Pipeline
   • Parse XML → Extract transactions
   • Clean & Normalize → Standardize formats
   • Categorize → Apply business rules
   • Validate → Route errors to dead letter
   ↓
3. Dual Storage
   • Valid data → SQLite Database (normalized tables)
   • Invalid data → Dead Letter Queue (for review)
   • Logs → etl.log (audit trail)
   ↓
4. Data Access Layer
   • Option A: Export aggregated data → dashboard.json
   • Option B: API endpoints → Real-time queries
   ↓
5. Frontend Visualization
   • Load data (from JSON or API)
   • Render charts, tables, analytics
   • Display to end user
```

### Design Decisions

**Why ETL Pattern?**
- Separates concerns: parsing, cleaning, and loading are independent
- Enables error handling at each stage
- Makes testing and debugging easier

**Why SQLite?**
- Lightweight, no separate server required
- Perfect for development and small-to-medium datasets
- Easy to backup (single file)

**Why dashboard.json?**
- Reduces database load for frequently accessed aggregations
- Faster frontend loading (no API/DB overhead)
- Can be version controlled for change tracking

**Why Dead Letter Queue?**
- Preserves problematic data for investigation
- Prevents data loss
- Helps identify data quality issues

### Error Handling Strategy

Our system implements comprehensive error handling:
- **Validation errors** → Logged with details in `etl.log`
- **Malformed XML** → Stored in `dead_letter/` for manual review
- **Processing failures** → Transaction rolled back, error logged
- **Database errors** → Graceful degradation, user notification

### Scalability Considerations

Current architecture supports:
- Thousands of transactions per run
- Multiple ETL executions per day
- Concurrent frontend users (via static files or API)

For enterprise-scale needs:
- Migrate SQLite → PostgreSQL/MySQL
- Add message queue (RabbitMQ/Kafka) for real-time processing
- Implement caching layer (Redis)
- Deploy API with load balancing

---

## Project Structure
```
├── README.md                         # Setup, run, overview
├── .env.example                      # DATABASE_URL or path to SQLite
├── requirements.txt                  # lxml/ElementTree, dateutil, (FastAPI optional)
├── index.html                        # Dashboard entry (static)
├── web/
│   ├── styles.css                    # Dashboard styling
│   ├── chart_handler.js              # Fetch + render charts/tables
│   └── assets/                       # Images/icons (optional)
├── data/
│   ├── raw/                          # Provided XML input (git-ignored)
│   │   └── momo.xml
│   ├── processed/                    # Cleaned/derived outputs for frontend
│   │   └── dashboard.json            # Aggregates the dashboard reads
│   ├── db.sqlite3                    # SQLite DB file
│   └── logs/
│       ├── etl.log                   # Structured ETL logs
│       └── dead_letter/              # Unparsed/ignored XML snippets
├── etl/
│   ├── __init__.py
│   ├── config.py                     # File paths, thresholds, categories
│   ├── parse_xml.py                  # XML parsing (ElementTree/lxml)
│   ├── clean_normalize.py            # Amounts, dates, phone normalization
│   ├── categorize.py                 # Simple rules for transaction types
│   ├── load_db.py                    # Create tables + upsert to SQLite
│   └── run.py                        # CLI: parse -> clean -> categorize -> load -> export JSON
├── api/                              # Optional (bonus)
│   ├── __init__.py
│   ├── app.py                        # Minimal FastAPI with /transactions, /analytics
│   ├── db.py                         # SQLite connection helpers
│   └── schemas.py                    # Pydantic response models
├── scripts/
│   ├── run_etl.sh                    # python etl/run.py --xml data/raw/momo.xml
│   ├── export_json.sh                # Rebuild data/processed/dashboard.json
│   └── serve_frontend.sh             # python -m http.server 8000 (or Flask static)
└── tests/
    ├── test_parse_xml.py             # Small unit tests
    ├── test_clean_normalize.py
    └── test_categorize.py
```
---

## References & Credits

### Tools Used
- **Eraser.io** - Architecture diagram design and generation
- **GitHub** - Version control and team collaboration
- **Jira** - Agile project management and sprint tracking

### Documentation
- Project structure inspired by industry best practices
- ETL patterns based on data engineering principles
