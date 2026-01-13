# MoMo-Data-Pipeline-Team-2

## Team 2 - MoMo SMS ETL Project
### Team Members
- Brian
- Derick
- Habibllah
- Yonas

---

## Links
- **Architecture Diagram:** [Link to image or file](https://drive.google.com/file/d/1_R2R9Gr6-Rh1-_83e8GfeI4qMhwHSEkr/view?usp=sharing)
- **Scrum Board:** [Team 2 Scrum Board](https://alustudent-team-k1plq8kl.atlassian.net/jira/software/projects/T2MSEP/boards/34?jql=&atlOrigin=eyJpIjoiN2ZkZGMzNjFhMTZkNGQzODg4MTM1YzI2ZGIyZDZiODAiLCJwIjoiaiJ9)

---

## Project Overview
An enterprise-level fullstack application to process MoMo SMS data (XML), categorize transactions, and visualize insights via a dashboard.

---

## Table of Contents (more to be added as we build up)

- [Project Structure](#project-structure)
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

