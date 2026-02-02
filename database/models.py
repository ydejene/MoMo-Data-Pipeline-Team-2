from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'Momo_User'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)
    username = Column(String(30), unique=True)
    password_text = Column(String(255), nullable=False)
    email_address = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    transactions = relationship("Transaction", back_populates="user")

class TransactionCategory(Base):
    __tablename__ = 'Transaction_Categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(30), nullable=False)
    category_code = Column(String(30), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    transactions = relationship("Transaction", back_populates="category")

class FeeType(Base):
    __tablename__ = 'Fee_Type'
    
    fee_type_id = Column(Integer, primary_key=True, autoincrement=True)
    fee_name = Column(String(50), nullable=False)
    
    transaction_fees = relationship("TransactionFee", back_populates="fee_type")

class Transaction(Base):
    __tablename__ = 'Transactions'
    
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    external_ref = Column(String(100), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(10), default='RWF', nullable=False)
    transaction_status = Column(String(30), default='COMPLETED', nullable=False)
    sender_notes = Column(Text)
    raw_data = Column(Text, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    counter_party = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    
    category_id = Column(Integer, ForeignKey('Transaction_Categories.category_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('Momo_User.user_id'), nullable=False)
    
    category = relationship("TransactionCategory", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    fees = relationship("TransactionFee", back_populates="transaction", cascade="all, delete-orphan")

class TransactionFee(Base):
    __tablename__ = 'Transaction_fees'
    
    transaction_fees_id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_fee_amount = Column(Numeric(15, 2), default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    transaction_id = Column(Integer, ForeignKey('Transactions.transaction_id'), nullable=False)
    fee_type_id = Column(Integer, ForeignKey('Fee_Type.fee_type_id'), nullable=False)
    
    transaction = relationship("Transaction", back_populates="fees")
    fee_type = relationship("FeeType", back_populates="transaction_fees")

class SystemLog(Base):
    __tablename__ = 'System_Logs'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    log_type = Column(String(30), nullable=False)
    raw_sms_body = Column(Text)
    severity = Column(String(30), default='INFO', nullable=False)
    log_time = Column(DateTime, default=datetime.now)