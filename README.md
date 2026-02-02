# MoMo-Data-Pipeline-Team-2

## Team 2 - MoMo SMS ETL & REST API Project
### Team Members
- **Brian** 
- **Derick** 
- **Habibllah** 
- **Yonas** 

---

## Quick Links
- **Architecture Diagram:** [View Architecture](./docs/images/architecture-diagram.png)
- **ERD Diagram:** [View ERD](./docs/images/erd_diagram.png)
- **ERD Design Rationale:** [Read Justification](./docs/ERD_justification.md)
- **API Documentation:** [View API Docs](./docs/api_docs.md)
- **Scrum Board:** [Team 2 Jira Board](https://alustudent-team-k1plq8kl.atlassian.net/jira/software/projects/T2MSEP/boards/34)

---

## Project Overview
An enterprise-level fullstack application to process MoMo SMS transaction data from XML format, store it in a relational database, and provide secure REST API access for transaction management and analytics.

**Key Features:**
- Complete ETL pipeline (Extract → Transform → Load)
- SQLAlchemy ORM with normalized database schema
- REST API with full CRUD operations
- Basic Authentication security
- DSA performance comparison (Linear Search vs Dictionary Lookup)
- Comprehensive error handling and logging

---

## Project Structure
```
MoMo-Data-Pipeline-Team-2/
├── api/                              # REST API Implementation
│   └── app.py                        # HTTP server with CRUD endpoints
│
├── data/                             # Data storage
│   ├── raw/
│   │   └── modified_sms_v2.xml       # Source SMS data (816KB, 1691 records)
│   ├── processed/                    # ETL intermediate outputs
│   │   ├── 01_extracted_raw.json     # Extracted SMS records
│   │   ├── 02_cleaned_normalized.json # Cleaned data
│   │   └── 03_categorized.json       # Categorized transactions
│   └── logs/
│       └── dead_letter/              # Failed/unparsed records
│
├── database/                         # Database layer
│   ├── models.py                     # SQLAlchemy ORM models
│   ├── db_config.py                  # Database connection & session
│   ├── init_db.py                    # Database initialization & seed data
│   ├── database_setup.sql            # SQL schema (Phase 2 deliverable)
│   └── db.sqlite3                    # SQLite database (generated, in .gitignore)
│
├── docs/                             # Documentation
│   ├── ERD_justification.md          # Database design rationale
│   ├── api_docs.md                   # API endpoint documentation
│   └── images/
│       ├── architecture-diagram.png  # System architecture
│       └── erd_diagram.png           # Entity relationship diagram
│
├── dsa/                              # Data Structures & Algorithms
│   └── search_comparison.py          # Performance comparison (Linear vs Dict)
│
├── etl/                              # ETL Pipeline
│   ├── parse_xml.py                  # Step 1: Extract raw SMS from XML
│   ├── clean_normalize.py            # Step 2: Clean & normalize data
│   ├── categorize.py                 # Step 3: Categorize transactions
│   ├── load_db.py                    # Step 4: Load to database
│   └── run.py                        # ETL orchestrator (run all steps)
│
├── examples/                         # JSON schemas
│   └── json_schemas.json             # Complete JSON schema definitions
│
├── screenshots/                      # API testing screenshots
│   ├── get_all_transactions.png
│   ├── get_single_transaction.png
│   ├── post_transaction.png
│   ├── put_transaction.png
│   ├── delete_transaction.png
│   └── unauthorized_401.png
│
├── .gitignore                        # Git ignore rules (includes *.sqlite3)
├── requirements.txt                  # Python dependencies
├── LICENSE                           # MIT License
└── README.md                         # This file
```

---

## System Architecture

### High-Level Data Flow
```
XML Source → ETL Pipeline → SQLite Database → REST API → Client Applications
```

### Architecture Components

#### 1️**Data Source Layer**
- **Input:** `modified_sms_v2.xml` (816KB, 1691 SMS records)
- **Format:** XML with MoMo transaction messages
- **Source:** Rwanda MTN Mobile Money SMS export

#### 2️**ETL Pipeline** Implemented
| Step | Script | Input | Output | Purpose |
|------|--------|-------|--------|---------|
| 1 | `parse_xml.py` | `modified_sms_v2.xml` | `01_extracted_raw.json` | Extract raw SMS attributes |
| 2 | `clean_normalize.py` | `01_extracted_raw.json` | `02_cleaned_normalized.json` | Clean types, convert dates |
| 3 | `categorize.py` | `02_cleaned_normalized.json` | `03_categorized.json` | Extract amounts, categorize |
| 4 | `load_db.py` | `03_categorized.json` | `db.sqlite3` | Save to database |

**Orchestration:** Run complete pipeline with `etl/run.py`

#### 3️**Storage Layer** Implemented
- **Database:** SQLite (`database/db.sqlite3`)
- **ORM:** SQLAlchemy with declarative models
- **Schema:** 6 normalized tables (see ERD)
  - `Momo_User` - User accounts
  - `Transaction_Categories` - Transaction types
  - `Transactions` - Main transaction records
  - `Fee_Type` - Fee type reference
  - `Transaction_fees` - Junction table (M:N)
  - `System_Logs` - Processing logs

#### 4️**API Layer** Implemented
- **Server:** Python `http.server.BaseHTTPRequestHandler`
- **Port:** 8000 (localhost)
- **Authentication:** HTTP Basic Auth
- **Format:** JSON responses
- **Endpoints:** 5 CRUD operations (see API Documentation)

#### 5️**DSA Layer** Implemented
- **Comparison:** Linear Search vs Dictionary Lookup
- **Dataset:** 20+ transactions from database
- **Iterations:** 10,000 per method
- **Visualization:** Matplotlib bar chart

---

## Database Design

### Entity Relationship Diagram
![ERD Diagram](docs/images/erd_diagram.png)

### Core Tables

**Momo_User**
- Stores user account information
- Primary Key: `user_id`
- Unique constraints: `phone_number`, `username`

**Transactions**
- Main transaction records with SMS data
- Foreign Keys: `user_id`, `category_id`
- Stores: amount, currency, status, raw SMS, dates

**Transaction_fees** (Junction Table)
- Resolves M:N relationship between Transactions and Fee_Type
- Composite unique key prevents duplicate fees per transaction

**System_Logs**
- Audit trail for ETL processing
- Tracks errors, batch operations, validation issues

### Design Rationale
[Read full justification](./docs/ERD_justification.md)

**Key Features:**
-  Third Normal Form (3NF) compliance
-  Referential integrity with CASCADE/RESTRICT
-  Check constraints (currency, status, amounts ≥ 0)
-  Strategic indexes (user_id, transaction_date, phone_number)
-  Many-to-many fee relationships

---

## Getting Started

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt
```

**Dependencies:**
- `sqlalchemy==2.0.23` - ORM and database toolkit
- `matplotlib==3.8.2` - Visualization for DSA comparison

### Installation & Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/your-org/MoMo-Data-Pipeline-Team-2.git
cd MoMo-Data-Pipeline-Team-2
```

#### Step 2: Initialize Database
```bash
cd database
python init_db.py

# Expected output:
# Creating database tables...
# ✓ Database created at: database/db.sqlite3
# Inserting seed data...
# ✓ Seed data inserted:
#   - 6 transaction categories
#   - 5 fee types
#   - 2 test users
```

#### Step 3: Run ETL Pipeline
```bash
cd ../etl
python run.py

# Expected output:
# Step 1: Extract (Parse XML)
# ✓ Extracted 1691 M-Money SMS records
# 
# Step 2: Transform (Clean & Normalize)
# ✓ Cleaned 1691 records
# 
# Step 3: Transform (Categorize)
# ✓ Categorized 1650 transactions
# 
# Step 4: Load (Save to Database)
# ✓ Successfully loaded 1650 transactions
```

#### Step 4: Start API Server
```bash
cd ../api
python app.py

# Expected output:
#    MoMo SMS API Server running at http://localhost:8000
#    Endpoints:
#    GET    /transactions       - List all transactions
#    GET    /transactions/{id}  - Get single transaction
#    POST   /transactions       - Create new transaction
#    PUT    /transactions/{id}  - Update transaction
#    DELETE /transactions/{id}  - Delete transaction
# 
#    Authentication: Basic Auth
#    Username: admin
#    Password: password123
```

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication
All endpoints require **HTTP Basic Authentication**

**Credentials:**
- Username: `admin`
- Password: `password123`

### Endpoints

#### 1. GET /transactions
**Description:** List all transactions (with optional filters)

**Request:**
```bash
curl -u admin:password123 http://localhost:8000/transactions

# With filters:
curl -u admin:password123 "http://localhost:8000/transactions?status=COMPLETED"
curl -u admin:password123 "http://localhost:8000/transactions?category=TRANSFER"
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 1650,
  "data": [
    {
      "transaction_id": 1,
      "external_ref": "76662021700",
      "amount": 2000.00,
      "currency": "RWF",
      "transaction_status": "COMPLETED",
      "transaction_date": "2024-05-10T16:30:51",
      "counter_party": "Jane Smith",
      "category": {
        "category_id": 1,
        "category_name": "Transfer",
        "category_code": "TRANSFER"
      },
      "user": {
        "user_id": 1,
        "full_name": "Admin User",
        "phone_number": "250788999999"
      },
      "fees": [
        {
          "fee_type": "Transaction Fee",
          "amount": 0.00
        }
      ]
    }
  ]
}
```

#### 2. GET /transactions/{id}
**Description:** Get single transaction by ID

**Request:**
```bash
curl -u admin:password123 http://localhost:8000/transactions/1
```

**Response (200 OK):** Same structure as single transaction above

**Error (404 Not Found):**
```json
{
  "error": "Not Found",
  "message": "Transaction 999 not found"
}
```

#### 3. POST /transactions
**Description:** Create new transaction

**Request:**
```bash
curl -X POST http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "external_ref": "TEST12345",
    "amount": 5000,
    "raw_data": "Test transaction SMS body",
    "transaction_date": "2024-01-20T10:00:00",
    "counter_party": "Test User",
    "category_code": "TRANSFER",
    "fee_amount": 50
  }'
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Transaction created successfully",
  "data": { ... }
}
```

#### 4. PUT /transactions/{id}
**Description:** Update existing transaction

**Request:**
```bash
curl -X PUT http://localhost:8000/transactions/1 \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 9999,
    "transaction_status": "COMPLETED",
    "sender_notes": "Updated note"
  }'
```

**Updateable Fields:**
- `amount`
- `transaction_status`
- `sender_notes`
- `counter_party`
- `currency`

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Transaction updated successfully",
  "data": { ... }
}
```

#### 5. DELETE /transactions/{id}
**Description:** Delete transaction

**Request:**
```bash
curl -X DELETE http://localhost:8000/transactions/1 \
  -u admin:password123
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Transaction 1 deleted successfully"
}
```

### Error Responses

**401 Unauthorized:**
```json
{
  "error": "Unauthorized",
  "message": "Valid credentials required"
}
```

**400 Bad Request:**
```json
{
  "error": "Bad Request",
  "message": "Invalid JSON in request body"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal Server Error",
  "message": "Database connection failed"
}
```

---

## Testing

### Manual Testing with curl

**Test successful authentication:**
```bash
curl -u admin:password123 http://localhost:8000/transactions
```

**Test unauthorized (wrong password):**
```bash
curl -u admin:wrongpassword http://localhost:8000/transactions
# Expected: 401 Unauthorized
```

**Test CRUD operations:**
```bash
# Create
curl -X POST ... (see POST example above)

# Read
curl -u admin:password123 http://localhost:8000/transactions/1

# Update
curl -X PUT ... (see PUT example above)

# Delete
curl -X DELETE -u admin:password123 http://localhost:8000/transactions/1
```

### DSA Performance Testing
```bash
cd dsa
python search_comparison.py

# Output:
# Testing Linear Search...
# Testing Dictionary Lookup...
# 
# ============================================================
# PERFORMANCE COMPARISON RESULTS
# ============================================================
# Linear Search Time:     0.234567 seconds
# Dictionary Lookup Time: 0.012345 seconds
# Speedup:                19.00x faster
# ============================================================
# 
# ✓ Chart saved to: dsa/search_comparison.png
```

---

## SQL Table to JSON Mapping

| SQL Table | JSON Representation | Relationship Handling |
|-----------|---------------------|----------------------|
| **Momo_User** | Flat object | Referenced by `user_id` FK |
| **Transaction_Categories** | Flat object | Referenced by `category_id` FK |
| **Fee_Type** | Flat object | Referenced by `fee_type_id` FK |
| **Transactions** | Nested object with `user` and `category` | FKs expanded to nested objects |
| **Transaction_fees** | Array in parent transaction | M:N resolved to `fees` array with nested `fee_type` |
| **System_Logs** | Flat object | Standalone, no relations |

**Mapping Strategy:**
- Foreign keys → Nested objects (reduces API calls)
- Many-to-many → Arrays with nested objects
- Computed fields (total_fees, total_cost) calculated on-the-fly

---

## Security

### Current Implementation: Basic Authentication

**How it works:**
1. Client encodes credentials as Base64: `base64(username:password)`
2. Sends in Authorization header: `Basic <base64-string>`
3. Server decodes and verifies against database
4. Returns 401 if invalid

**Weaknesses:**
- Base64 is encoding, NOT encryption (easily reversible)
- Credentials sent with every request
- No session management or token expiration
- Vulnerable to man-in-the-middle attacks without HTTPS

### Recommended Improvements

**For Production:**
1. **Use JWT (JSON Web Tokens)**
   - Stateless authentication with expiration
   - Include user roles/permissions in payload
   - Industry standard for REST APIs

2. **Implement HTTPS/TLS**
   - Encrypt all traffic
   - Prevent credential interception

3. **Hash Passwords**
   - Use bcrypt or argon2
   - Never store plain text (current demo uses plain text)

4. **Add Rate Limiting**
   - Prevent brute force attacks
   - Max 5 failed attempts per minute

5. **Consider OAuth 2.0**
   - For third-party API access
   - Separates authentication from authorization

---

## Performance & Scalability

### Current Capacity
- Handles 1,650+ transactions
- Supports concurrent API requests
- Dictionary lookup: O(1) vs Linear search: O(n)

### Optimization Strategies
- **Database:** Indexed columns (user_id, transaction_date, category_id)
- **API:** Efficient SQLAlchemy queries with joins
- **Caching:** Could add Redis for frequently accessed data

### Future Enhancements
- **Pagination:** Limit large result sets (e.g., 50 per page)
- **Database Migration:** SQLite → PostgreSQL for production
- **Horizontal Scaling:** Load balancer + multiple API instances
- **Message Queue:** RabbitMQ/Kafka for real-time processing

---

## Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **SQLAlchemy 2.0** - ORM and database toolkit
- **http.server** - Built-in HTTP server (no Flask/FastAPI)
- **SQLite** - Embedded relational database

### Data Processing
- **xml.etree.ElementTree** - XML parsing
- **re (regex)** - Transaction detail extraction
- **json** - Data serialization

### Visualization & Analysis
- **Matplotlib** - DSA performance charts
- **time** module - Performance measurement

### Development Tools
- **Git/GitHub** - Version control
- **Jira** - Agile project management
- **Eraser.io** - Architecture diagrams
- **curl/Postman** - API testing

---

## References & Credits

### Tools
- **Eraser.io** - Architecture diagram design
- **GitHub** - Version control and collaboration
- **Jira** - Sprint tracking and task management

### Learning Resources
- SQLAlchemy Official Documentation
- Python http.server Documentation
- JSON Schema Specification (Draft 07)
- ETL Best Practices (Data Engineering)

---

## AI Usage Attribution

### Policy Compliance
This project was developed by **Team 2** in full compliance with academic integrity policies. All code, database schemas, and technical implementations were designed and written by team members. AI tools (ChatGPT, Google Gemini) were used **exclusively for research, learning, and conceptual understanding** - not for generating implementation code.

### AI-Assisted Research Areas
1. **Database Design** - Researched normalization, indexing, foreign key patterns
2. **JSON Schema Standards** - Learned JSON Schema specification syntax
3. **ETL Architecture** - Studied pipeline patterns, error handling strategies
4. **REST API Conventions** - Researched HTTP status codes, authentication methods
5. **DSA Concepts** - Understood time complexity analysis (O(1) vs O(n))

**All implementation code was written by team members.**

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Team Contributions

| Member | Role | Contributions |
|--------|------|---------------|
| **Brian** | API Developer | PUT/DELETE endpoints, authentication logic |
| **Derick** | ETL Engineer | XML parsing, data cleaning pipeline |
| **Habibllah** | Database Architect | SQLAlchemy models, schema design, DSA implementation |
| **Yonas** | API Developer | GET/POST endpoints, error handling |

**Team Collaboration:**
- Daily standups via Jira
- Code reviews before merging
- Pair programming for complex features
- Shared documentation responsibilities

---

## Contact & Support

**Project Repository:** [GitHub - MoMo-Data-Pipeline-Team-2](https://github.com/your-org/MoMo-Data-Pipeline-Team-2)

**Scrum Board:** [Team 2 Jira](https://alustudent-team-k1plq8kl.atlassian.net/jira/software/projects/T2MSEP/boards/34)

For questions or issues, please create a GitHub issue or contact the team via Jira.

---

**Built with by Team 2 | January 2026**