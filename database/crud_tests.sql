-- CRUD Tests for MoMo Database
-- This file demonstrates Create, Read, Update, Delete operations.

-- =========================
-- CREATE (INSERT)
-- =========================

-- Insert a user (if user table exists and allows these columns)
INSERT INTO Momo_User (user_id, full_name, email_address, phone_number, username, password_text, created_at)
VALUES (1, 'John Doe', 'john.doe@example.com', '250788123456', 'johndoe', 'hashed_password_placeholder', CURRENT_TIMESTAMP);

-- Insert categories
INSERT INTO Transaction_Categories (category_id, category_name, category_code, is_active)
VALUES
(1, 'Transfer', 'TRANSFER', TRUE),
(2, 'Airtime', 'AIRTIME', TRUE);

-- Insert fee types
INSERT INTO Fee_Type (fee_type_id, fee_name)
VALUES
(1, 'Transaction Fee'),
(2, 'Tax');

-- Insert a transaction
INSERT INTO Transactions (transaction_id, external_ref, amount, currency, transaction_status, sender_notes, raw_data, transaction_date, counter_party, created_at, category_id, user_id)
VALUES
(1, '76662021700', 2000.00, 'RWF', 'COMPLETED', 'Rent payment',
 'You have received 2000 RWF from Jane Smith...', CURRENT_TIMESTAMP, 'Jane Smith', CURRENT_TIMESTAMP, 1, 1);

-- Insert transaction fees (junction table)
INSERT INTO Transaction_fees (transaction_fees_id, transaction_fee_amount, created_at, transaction_id, fee_type_id)
VALUES
(1, 100.00, CURRENT_TIMESTAMP, 1, 1),
(2, 50.00, CURRENT_TIMESTAMP, 1, 2);

-- =========================
-- READ (SELECT)
-- =========================

-- View all transactions with user and category
SELECT
  t.transaction_id,
  t.external_ref,
  t.amount,
  t.currency,
  t.transaction_status,
  u.full_name AS user_name,
  c.category_name
FROM Transactions t
JOIN Momo_User u ON t.user_id = u.user_id
JOIN Transaction_Categories c ON t.category_id = c.category_id;

-- View fees for a transaction
SELECT
  tf.transaction_fees_id,
  tf.transaction_fee_amount,
  ft.fee_name
FROM Transaction_fees tf
JOIN Fee_Type ft ON tf.fee_type_id = ft.fee_type_id
WHERE tf.transaction_id = 1;

-- =========================
-- UPDATE
-- =========================

-- Update transaction status
UPDATE Transactions
SET transaction_status = 'FAILED'
WHERE transaction_id = 1;

-- =========================
-- DELETE
-- =========================

-- Delete a fee record (safe delete example)
DELETE FROM Transaction_fees
WHERE transaction_fees_id = 2;
