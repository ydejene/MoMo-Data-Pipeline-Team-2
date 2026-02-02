# MoMo SMS API Documentation

## Authentication
All API endpoints require Basic Authentication.
- **Username**: `admin`
- **Password**: `password123`

Include the `Authorization` header in all requests:
`Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=`

---

## Endpoints

### 1. List All Transactions
Retrieve a paginated list of transactions with optional filtering.

**Endpoint & Method**
`GET /transactions`

**Query Parameters**
| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by transaction status (e.g., `COMPLETED`, `FAILED`) |
| `category` | string | Filter by category code (e.g., `TRANSFER`, `PAYMENT`) |

**Request Example**
```http
GET /transactions?status=COMPLETED&category=TRANSFER HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

**Response Example**
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "transaction_id": 1,
      "external_ref": "REF123456789",
      "amount": 5000.0,
      "currency": "RWF",
      "transaction_status": "COMPLETED",
      "sender_notes": "Lunch payment",
      "transaction_date": "2023-10-27T10:30:00",
      "counter_party": "John Doe",
      "created_at": "2023-10-27T10:35:00.123456",
      "category": {
        "category_id": 1,
        "category_name": "Transfers",
        "category_code": "TRANSFER"
      },
      "user": {
        "user_id": 1,
        "full_name": "Admin User",
        "phone_number": "+250780000000"
      },
      "fees": [
        {
          "fee_type": "Transaction Fee",
          "amount": 100.0
        }
      ]
    }
  ]
}
```

**Error Codes**
| Code | Description |
|------|-------------|
| `200` | Success |
| `401` | Unauthorized - Invalid credentials |
| `500` | Internal Server Error |

---

### 2. Get Single Transaction
Retrieve detailed information for a specific transaction by ID.

**Endpoint & Method**
`GET /transactions/{id}`

**Path Parameters**
| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Unique ID of the transaction |

**Request Example**
```http
GET /transactions/1 HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

**Response Example**
```json
{
  "success": true,
  "data": {
    "transaction_id": 1,
    "external_ref": "REF123456789",
    "amount": 5000.0,
    "currency": "RWF",
    "transaction_status": "COMPLETED",
    "sender_notes": "Lunch payment",
    "transaction_date": "2023-10-27T10:30:00",
    "counter_party": "John Doe",
    "created_at": "2023-10-27T10:35:00.123456",
    "category": {
      "category_id": 1,
      "category_name": "Transfers",
      "category_code": "TRANSFER"
    },
    "user": {
      "user_id": 1,
      "full_name": "Admin User",
      "phone_number": "+250780000000"
    },
    "fees": [
      {
        "fee_type": "Transaction Fee",
        "amount": 100.0
      }
    ]
  }
}
```

**Error Codes**
| Code | Description |
|------|-------------|
| `200` | Success |
| `401` | Unauthorized - Invalid credentials |
| `404` | Not Found - Transaction ID does not exist |
| `500` | Internal Server Error |

---

### 3. Create New Transaction
Create a new transaction record in the database.

**Endpoint & Method**
`POST /transactions`

**Request Body Parameters**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `external_ref` | string | Yes | External reference/transaction ID |
| `amount` | number | Yes | Transaction amount |
| `raw_data` | string | Yes | Original SMS or raw transaction data |
| `transaction_date` | string | Yes | Date and time in ISO 8601 format (e.g., `2024-01-15T14:30:00`) |
| `currency` | string | No | Currency code. Default: `RWF` |
| `category_code` | string | No | Transaction category (e.g., `TRANSFER`, `PAYMENT`, `DEPOSIT`). Default: `TRANSFER` |
| `transaction_status` | string | No | Status of transaction (e.g., `COMPLETED`, `PENDING`, `FAILED`). Default: `COMPLETED` |
| `sender_notes` | string | No | Notes from sender |
| `counter_party` | string | No | Recipient/counter party details |
| `fee_amount` | number | No | Transaction fee amount |

**Request Example**
```http
POST /transactions HTTP/1.1
Host: localhost:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
Content-Type: application/json
Content-Length: 245

{
  "external_ref": "MOM202401001",
  "amount": 5000,
  "raw_data": "You have transferred 5000 RWF to John Doe (0712345678). Fee: 50 RWF. New balance: 15000 RWF",
  "transaction_date": "2024-01-15T14:30:00",
  "currency": "RWF",
  "category_code": "TRANSFER",
  "transaction_status": "COMPLETED",
  "sender_notes": "Payment for goods",
  "counter_party": "John Doe (0712345678)",
  "fee_amount": 50
}
```

**Response Example (201 Created)**
```json
{
  "success": true,
  "message": "Transaction created successfully",
  "data": {
    "transaction_id": 1,
    "external_ref": "MOM202401001",
    "amount": 5000.0,
    "currency": "RWF",
    "transaction_status": "COMPLETED",
    "sender_notes": "Payment for goods",
    "transaction_date": "2024-01-15T14:30:00",
    "counter_party": "John Doe (0712345678)",
    "created_at": "2024-02-01T10:45:22.123456",
    "category": {
      "category_id": 1,
      "category_name": "Transfer",
      "category_code": "TRANSFER"
    },
    "user": {
      "user_id": 1,
      "full_name": "System User",
      "phone_number": "0700000000"
    },
    "fees": [
      {
        "fee_type": "Transaction Fee",
        "amount": 50.0
      }
    ]
  }
}
```

**Error Codes**
| Code | Description |
|------|-------------|
| `201` | Created - Transaction successfully created |
| `400` | Bad Request - Invalid JSON, missing required fields, or empty body |
| `401` | Unauthorized - Invalid credentials |
| `500` | Internal Server Error - Database error or invalid date format |
