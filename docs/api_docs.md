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
