-- MoMo SMS Data Processing System - Database Setup
DROP DATABASE IF EXISTS momo_sms_db;
CREATE DATABASE momo_sms_db; 
USE momo_sms_db;

-- Drop existing tables (for clean re-runs)
DROP TABLE IF EXISTS Transaction_fees;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Transaction_Categories;
DROP TABLE IF EXISTS Fee_Type;
DROP TABLE IF EXISTS System_Logs;
DROP TABLE IF EXISTS Momo_User;

-- 1. MOMO_USER TABLE

CREATE TABLE Momo_User (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique user identifier',
    full_name VARCHAR(255) NOT NULL COMMENT 'User full name',
    email_address VARCHAR(255) COMMENT 'Optional email address',
    phone_number VARCHAR(12) NOT NULL UNIQUE COMMENT 'Mobile money phone number',
    username VARCHAR(30) UNIQUE COMMENT 'Optional username for login',
    password_text VARCHAR(255) NOT NULL COMMENT 'Text password (not hashed) for basic authentication',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation timestamp',
    
    INDEX idx_phone_number (phone_number),
    INDEX idx_username (username)
) COMMENT = 'Stores mobile money user information';

-- 2. TRANSACTION_CATEGORIES TABLE

CREATE TABLE Transaction_Categories (
    category_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique category identifier',
    category_name VARCHAR(30) NOT NULL COMMENT 'Display name for category',
    category_code VARCHAR(30) NOT NULL UNIQUE COMMENT 'Internal code for application logic',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Whether category is currently active',
    
    INDEX idx_category_code (category_code)
) COMMENT = 'Reference table for transaction types';

-- 3. TRANSACTIONS TABLE

CREATE TABLE Transactions (
    transaction_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique transaction identifier',
    external_ref VARCHAR(100) NOT NULL COMMENT 'External transaction reference from SMS',
    amount DECIMAL(15, 2) NOT NULL COMMENT 'Transaction amount',
    currency VARCHAR(10) NOT NULL DEFAULT 'RWF' COMMENT 'Currency code (RWF, ETB, etc.)',
    transaction_status VARCHAR(30) NOT NULL DEFAULT 'COMPLETED' COMMENT 'Transaction status',
    sender_notes TEXT COMMENT 'Optional transaction notes or message from sender',
    raw_data TEXT NOT NULL COMMENT 'Original SMS message body',
    transaction_date DATETIME(3) NOT NULL COMMENT 'When transaction actually occurred',
    counter_party VARCHAR(255) COMMENT 'Name of other party in transaction',
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT 'Database insertion timestamp',
    
    -- Foreign Keys
    category_id BIGINT NOT NULL COMMENT 'Transaction category',
    user_id BIGINT NOT NULL COMMENT 'Mobile money user',
    
    FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Momo_User(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    
    -- Constraints
    CHECK (amount >= 0),
    CHECK (currency IN ('RWF', 'ETB', 'USD')),
    CHECK (transaction_status IN ('COMPLETED', 'FAILED', 'PENDING')),
    
    -- Indexes for performance
    INDEX idx_user_id (user_id),
    INDEX idx_category_id (category_id),
    INDEX idx_transaction_date (transaction_date),
    INDEX idx_transaction_status (transaction_status),
    INDEX idx_external_ref (external_ref)
) COMMENT = 'Main transaction records from SMS data';

-- 4. FEE_TYPE TABLE

CREATE TABLE Fee_Type (
    fee_type_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique fee type identifier',
    fee_name VARCHAR(50) NOT NULL COMMENT 'Fee type name (e.g., Transaction Fee, Tax)',
    
    INDEX idx_fee_name (fee_name)
) COMMENT = 'Reference table for fee types';

-- 5. TRANSACTION_FEES TABLE (Junction Table)

CREATE TABLE Transaction_fees (
    transaction_fees_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique fee record identifier',
    transaction_fee_amount DECIMAL(15, 2) NOT NULL DEFAULT 0 COMMENT 'Actual fee amount charged',
    created_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT 'Fee record creation timestamp',
    
    -- Foreign Keys
    transaction_id BIGINT NOT NULL COMMENT 'Reference to parent transaction',
    fee_type_id BIGINT NOT NULL COMMENT 'Type of fee applied',
    
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (fee_type_id) REFERENCES Fee_Type(fee_type_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    
    -- Constraints
    CHECK (transaction_fee_amount >= 0),
    
    -- Indexes
    INDEX idx_transaction_id (transaction_id),
    INDEX idx_fee_type_id (fee_type_id),
    
    -- Prevent duplicate fee types for same transaction
    UNIQUE KEY unique_transaction_fee (transaction_id, fee_type_id)
) COMMENT = 'Junction table resolving M:N relationship between transactions and fee types';

-- 6. SYSTEM_LOGS TABLE

CREATE TABLE System_Logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique log entry identifier',
    log_type VARCHAR(30) NOT NULL COMMENT 'Type of log entry (PARSE_ERROR, DB_ERROR, etc.)',
    raw_sms_body TEXT COMMENT 'Raw SMS content if parsing error occurred',
    severity VARCHAR(30) NOT NULL DEFAULT 'INFO' COMMENT 'Log severity level',
    log_time DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT 'When log entry was created',
    
    CHECK (severity IN ('ERROR', 'WARNING', 'INFO')),
    CHECK (log_type IN ('PARSE_ERROR', 'DB_ERROR', 'VALIDATION_ERROR', 'BATCH_START', 'BATCH_COMPLETE')),
    
    INDEX idx_log_type (log_type),
    INDEX idx_severity (severity),
    INDEX idx_log_time (log_time)
) COMMENT = 'System processing logs for debugging and monitoring';