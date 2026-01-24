-- MoMo SMS Data Processing System - Database Setup

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