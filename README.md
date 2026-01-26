# MoMo-Data-Pipeline-Team-2

## Team 2 - MoMo SMS ETL Project
### Team Members
- Brian
- Derick
- Habibllah
- Yonas

---

## Links
- **Architecture Diagram:** [Link to Architecture Diagram](./docs/images/architecture-diagram.png)
- **ERD Diagram:** [View ERD](./docs/images/erd_diagram.png)
- **ERD Design Rationale:** [Read Justification](./docs/ERD_justification.md)
- **Scrum Board:** [Team 2 Scrum Board](https://alustudent-team-k1plq8kl.atlassian.net/jira/software/projects/T2MSEP/boards/34?jql=&atlOrigin=eyJpIjoiN2ZkZGMzNjFhMTZkNGQzODg4MTM1YzI2ZGIyZDZiODAiLCJwIjoiaiJ9)

---

## Project Overview
An enterprise-level fullstack application to process MoMo SMS data (XML), categorize transactions, and visualize insights via a dashboard.

---

## Table of Contents (more to be added as we build up)

- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [Database Design](#database-design)
---

## Project Structure

```
MoMo-Data-Pipeline-Team-2/
├── .git/                             # Git version control
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
├── README.md                         # Project documentation
│
├── api/                              # API layer (placeholder for future development)
│   └── .gitkeep
│
├── data/                             # Data storage directory
│   ├── raw/                          # Raw input data
│   │   ├── .gitkeep
│   │   └── modified_sms_v2.xml       # Raw MoMo SMS data (816KB)
│   ├── processed/                    # Processed data outputs
│   │   └── .gitkeep
│   └── logs/                         # Processing logs
│       └── dead_letter/              # Failed/unparsed records
│           └── .gitkeep
│
├── database/                         # Database schema and setup
│   └── database_setup.sql            # Complete database DDL and sample data
│
├── docs/                             # Documentation
│   ├── ERD_justification.md          # Database design rationale
│   └── images/                       # Diagrams and visuals
│       ├── architecture-diagram.png  # System architecture diagram
│       └── erd_diagram.png           # Entity relationship diagram
│
├── etl/                              # ETL pipeline (placeholder for future development)
│   └── .gitkeep
│
├── examples/                         # Example schemas and data models
│   └── json_schemas.json             # JSON schemas for all database entities
│
├── scripts/                          # Automation scripts (placeholder for future development)
│   └── .gitkeep
│
├── tests/                            # Test suite (placeholder for future development)
│   └── .gitkeep
│
└── web/                              # Frontend dashboard (placeholder for future development)
    └── assets/
        └── .gitkeep
```
---

## System Architecture

### High-Level Overview
Our system follows a layered architecture pattern with clear separation of concerns:
- **Data Ingestion** → **Processing** → **Storage** → **API/Export** → **Visualization**

[Link to Architecture Diagram](./docs/architecture-diagram.png)

### Architecture Components

#### 1️⃣ Data Source Layer
| Component | Purpose | Technology |
|-----------|---------|------------|
| `modified_sms_v2.xml` | Raw MoMo SMS transaction data in XML format (816KB) | XML |

#### 2️⃣ ETL Pipeline (Planned - Not Yet Implemented)
| Component | Planned File | Purpose |
|-----------|-------------|---------|
| **XML Parser** | `etl/parse_xml.py` | Will read and validate XML structure, extract transaction records |
| **Data Cleaner** | `etl/clean_normalize.py` | Will normalize amounts, standardize date formats, normalize phone numbers |
| **Categorizer** | `etl/categorize.py` | Will apply business rules to classify transactions |
| **Error Handler** | Built into pipeline | Will capture malformed/invalid data and route to dead letter queue |
| **ETL Orchestrator** | `etl/run.py` | Planned CLI tool to coordinate the entire ETL workflow |
| **Logger** | `data/logs/*.log` | Will record all ETL operations, errors, and audit trail |

> **Status:** ETL directory currently contains only placeholder `.gitkeep` file. Implementation pending.

#### 3️⃣ Storage Layer
| Component | File/Location | Purpose | Status |
|-----------|---------------|---------|--------|
| **Database Schema** | `database/database_setup.sql` | Complete MySQL database schema with DDL and sample data | ✅ Implemented |
| **Raw Data** | `data/raw/modified_sms_v2.xml` | Original MoMo SMS transaction data in XML format | ✅ Available |
| **Processed Data** | `data/processed/` | Directory for processed outputs (currently empty) | 📁 Ready |
| **Dead Letter Queue** | `data/logs/dead_letter/` | Directory for failed/unparsed records | 📁 Ready |

#### 4️⃣ API Layer (Planned - Not Yet Implemented)
| Component | Planned File | Purpose |
|-----------|-------------|---------|
| **FastAPI Backend** | `api/app.py` | Will provide RESTful API server for transaction data access |
| **Planned Endpoints** | | • `GET /transactions` - Retrieve filtered transaction list<br>• `GET /analytics` - Get aggregated statistics<br>• `GET /categories` - List transaction categories |
| **Database Helper** | `api/db.py` | Will handle database connection pool and query utilities |
| **Data Schemas** | `api/schemas.py` | Will define Pydantic models for request/response validation |

> **Status:** API directory currently contains only placeholder `.gitkeep` file. Implementation pending.

#### 5️⃣ Presentation Layer (Planned - Not Yet Implemented)
| Component | Planned File | Purpose |
|-----------|-------------|---------|
| **Dashboard UI** | `index.html` | Will provide main user interface for viewing transactions and analytics |
| **Visualization Engine** | `web/chart_handler.js` | Will fetch data and render interactive charts and tables |
| **Styling** | `web/styles.css` | Will provide responsive design and visual styling |
| **Assets** | `web/assets/` | Directory for icons, images, and static resources |

> **Status:** Web directory currently contains only placeholder structure. Implementation pending.

#### 6️⃣ Automation Scripts (Planned - Not Yet Implemented)
| Planned Script | Purpose | Planned Usage |
|----------------|---------|---------------|
| `scripts/run_etl.sh` | Will execute the complete ETL pipeline from XML to database | `./scripts/run_etl.sh` |
| `scripts/export_json.sh` | Will regenerate dashboard data with latest aggregations | `./scripts/export_json.sh` |
| `scripts/serve_frontend.sh` | Will start local development server for testing | `./scripts/serve_frontend.sh` |

> **Status:** Scripts directory currently contains only placeholder `.gitkeep` file. Implementation pending.

### Data Flow (Planned Architecture)
```
1. XML File (modified_sms_v2.xml) 
   ↓
2. ETL Pipeline (To Be Implemented)
   • Parse XML → Extract transactions
   • Clean & Normalize → Standardize formats
   • Categorize → Apply business rules
   • Validate → Route errors to dead letter
   ↓
3. Dual Storage
   • Valid data → Database (schema defined in database_setup.sql)
   • Invalid data → Dead Letter Queue (for review)
   • Logs → Processing logs (audit trail)
   ↓
4. Data Access Layer (To Be Implemented)
   • Option A: Export aggregated data → dashboard.json
   • Option B: API endpoints → Real-time queries
   ↓
5. Frontend Visualization (To Be Implemented)
   • Load data (from JSON or API)
   • Render charts, tables, analytics
   • Display to end user
```

### Current Project Status

#### ✅ Completed
1. **Database Design**
   - Complete MySQL schema with 6 normalized tables
   - Foreign key relationships and constraints defined
   - Sample data for testing (7 users, 6 categories, 5 fee types, 9 transactions)
   - Full DDL in `database/database_setup.sql`

2. **Data Modeling**
   - JSON schemas for all database entities
   - Example API response structures
   - Complete transaction object with nested relationships
   - Documented in `examples/json_schemas.json`

3. **Documentation**
   - Entity Relationship Diagram (ERD)
   - Architecture diagram
   - Database design rationale
   - Project structure and planning documents

4. **Raw Data**
   - MoMo SMS transaction data available (816KB XML file)
   - Ready for ETL processing

#### 🔴 Pending Implementation
1. **ETL Pipeline** - XML parsing, data cleaning, categorization, and database loading
2. **REST API** - FastAPI backend with transaction and analytics endpoints
3. **Frontend Dashboard** - Web interface for data visualization
4. **Automation Scripts** - Shell scripts for running ETL and serving the application
5. **Testing Suite** - Unit and integration tests for all components

### Design Decisions

**Why ETL Pattern?**
- Will separate concerns: parsing, cleaning, and loading as independent stages
- Enables error handling at each stage
- Makes testing and debugging easier

**Why MySQL?**
- Industry-standard relational database
- Robust support for complex queries and transactions
- Excellent for structured financial data
- Easy to migrate to cloud-hosted MySQL (AWS RDS, Google Cloud SQL)

**Why JSON Schemas?**
- Provides clear API response format documentation
- Enables frontend-backend contract validation
- Demonstrates how relational data will be serialized
- Useful for API development and testing

**Why Dead Letter Queue?**
- Will preserve problematic data for investigation
- Prevents data loss
- Helps identify data quality issues in SMS parsing

### Error Handling Strategy (Planned)

The system will implement comprehensive error handling:
- **Validation errors** → Logged with details
- **Malformed XML** → Stored in `dead_letter/` for manual review
- **Processing failures** → Transaction rolled back, error logged
- **Database errors** → Graceful degradation, user notification

### Scalability Considerations

Current architecture design supports:
- Thousands of transactions per run
- Multiple ETL executions per day
- Concurrent frontend users (via static files or API)

For enterprise-scale needs:
- MySQL already supports production workloads
- Can add message queue (RabbitMQ/Kafka) for real-time processing
- Can implement caching layer (Redis)
- Can deploy API with load balancing

---

## Database Design

### Entity Relationship Diagram
![ERD Diagram](docs/images/erd_diagram.png)

### Design Rationale
[Read the full ERD design justification](./docs/ERD_justification.md)

Our database is built around the core idea that every MoMo transaction involves an individual, a transaction type, and potentially multiple fees. 

### Key Features
- **Normalized schema** with proper primary and foreign key relationships
- **Junction table** (`Transaction_fees`) resolving many-to-many fee relationships
- **Check constraints** ensuring data validity (currency codes, status values, non-negative amounts)
- **Indexes** on frequently queried columns (user_id, transaction_date, phone_number)
- **Audit trail** via raw SMS storage and system logs

## References & Credits

### Tools Used
- **Eraser.io** - Architecture diagram design and generation
- **GitHub** - Version control and team collaboration
- **Jira** - Agile project management and sprint tracking

### Documentation
- Project structure inspired by industry best practices
- ETL patterns based on data engineering principles
