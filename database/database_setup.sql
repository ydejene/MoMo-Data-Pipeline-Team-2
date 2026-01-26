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

-- SAMPLE DATA INSERTION (DML)
-- Insert sample users 
INSERT INTO Momo_User (full_name, email_address, phone_number, username, password_text) VALUES
('John Doe', 'john.doe@example.com', '250788123456', 'johndoe', 'password123'),
('Jane Smith', 'jane.smith@example.com', '250788234567', 'janesmith', 'password456'),
('Bob Wilson', 'bob.wilson@example.com', '250788345678', 'bobwilson', 'password789'),
('Alice Johnson', 'alice.j@example.com', '250788456789', 'alicej', 'passwordABC'),
('Samuel Carter', 'sam.carter@example.com', '250788567890', 'samcarter', 'passwordDEF'),
('Emma Brown', NULL, '250788678901', 'emmab', 'passwordGHI'),
('David Lee', NULL, '250788789012', 'davidlee', 'passwordJKL');

-- Insert transaction categories (at least 5)
INSERT INTO Transaction_Categories (category_name, category_code, is_active) VALUES
('Transfer', 'TRANSFER', TRUE),
('Payment', 'PAYMENT', TRUE),
('Deposit', 'DEPOSIT', TRUE),
('Withdrawal', 'WITHDRAWAL', TRUE),
('Airtime Purchase', 'AIRTIME', TRUE),
('Bill Payment', 'BILL_PAYMENT', TRUE),
('Bundle purchase', 'BUNDLE_PURCHASE', TRUE);

-- Insert fee types (at least 5)
INSERT INTO Fee_Type (fee_name) VALUES
('Transaction Fee'),
('Tax'),
('Service Charge'),
('Agent Commission'),
('Processing Fee');

-- Insert sample transactions (at least 5)
INSERT INTO Transactions (external_ref, amount, currency, transaction_status, sender_notes, raw_data, transaction_date, counter_party, category_id, user_id) VALUES
('76662021700', 2000.00, 'RWF', 'COMPLETED', '', 'You have received 2000 RWF from Jane Smith (*********013) on your mobile money account at 2024-05-10 16:30:51. Message from sender: . Your new balance:2000 RWF. Financial Transaction Id: 76662021700.', '2024-05-10 16:30:51', 'Jane Smith', 1, 1),
('73214484437', 1000.00, 'RWF', 'COMPLETED', '', 'TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith 12845 has been completed at 2024-05-10 16:31:39. Your new balance: 1,000 RWF. Fee was 0 RWF.', '2024-05-10 16:31:39', 'Jane Smith', 2, 2),
('51732411227', 600.00, 'RWF', 'COMPLETED', '', 'TxId: 51732411227. Your payment of 600 RWF to Samuel Carter 95464 has been completed at 2024-05-10 21:32:32. Your new balance: 400 RWF. Fee was 0 RWF.', '2024-05-10 21:32:32', 'Samuel Carter', 2, 3),
('DEPOSIT001', 40000.00, 'RWF', 'COMPLETED', '', '*113*R*A bank deposit of 40000 RWF has been added to your mobile money account at 2024-05-11 18:43:49. Your NEW BALANCE :40400 RWF. Cash Deposit::CASH::::0::250795963036.', '2024-05-11 18:43:49', 'Bank Deposit', 3, 1),
('TXN12345', 5000.00, 'RWF', 'COMPLETED', 'Rent payment', 'Transfer of 5000 RWF completed successfully for rent payment.', '2024-05-12 09:15:00', 'Bob Wilson', 1, 1),
('TXN12346', 1500.00, 'RWF', 'COMPLETED', 'Birthday gift', 'Payment of 1500 RWF to Alice Johnson for birthday gift.', '2024-05-12 14:22:00', 'Alice Johnson', 2, 3),
('TXN12347', 300.00, 'RWF', 'COMPLETED', NULL, 'Airtime purchase of 300 RWF completed successfully.', '2024-05-13 08:45:00', 'MTN Rwanda', 5, 4),
('TXN12348', 2500.00, 'RWF', 'PENDING', NULL, 'Bill payment pending confirmation.', '2024-05-14 10:00:00', 'EUCL', 6, 5),
('TXN12349', 800.00, 'RWF', 'FAILED', NULL, 'Transaction failed due to insufficient balance.', '2024-05-14 15:30:00', 'Emma Brown', 1, 6);

-- Insert transaction fees (M:N relationship - at least 5)
INSERT INTO Transaction_fees (transaction_id, fee_type_id, transaction_fee_amount) VALUES
(1, 1, 0.00),   -- Transaction 1: Transaction Fee = 0
(1, 2, 0.00),   -- Transaction 1: Tax = 0
(2, 1, 0.00),   -- Transaction 2: Transaction Fee = 0
(3, 1, 0.00),   -- Transaction 3: Transaction Fee = 0
(4, 1, 100.00), -- Transaction 4: Transaction Fee = 100
(4, 2, 50.00),  -- Transaction 4: Tax = 50
(5, 1, 50.00),  -- Transaction 5: Transaction Fee = 50
(5, 2, 25.00),  -- Transaction 5: Tax = 25
(6, 1, 25.00),  -- Transaction 6: Transaction Fee = 25
(7, 1, 10.00),  -- Transaction 7: Transaction Fee = 10
(8, 1, 30.00),  -- Transaction 8: Transaction Fee = 30
(9, 1, 15.00);  -- Transaction 9: Transaction Fee = 15 (failed transaction still had fee attempt)

-- Insert system logs (at least 5)
INSERT INTO System_Logs (log_type, raw_sms_body, severity, log_time) VALUES
('BATCH_START', NULL, 'INFO', '2024-05-10 16:00:00'),
('BATCH_COMPLETE', NULL, 'INFO', '2024-05-10 16:05:00'),
('PARSE_ERROR', 'TxId: INVALID. Amount field missing from SMS body.', 'ERROR', '2024-05-11 10:30:00'),
('VALIDATION_ERROR', NULL, 'WARNING', '2024-05-12 14:15:00'),
('DB_ERROR', NULL, 'ERROR', '2024-05-13 09:00:00'),
('BATCH_START', NULL, 'INFO', '2024-05-14 08:00:00'),
('PARSE_ERROR', 'Your payment of INVALID RWF... malformed amount string', 'ERROR', '2024-05-14 11:22:00');
