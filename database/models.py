from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'Momo_User'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)
    username = Column(String(30), unique=True)
    password_text = Column(String(255), nullable=False)
    email_address = Column(String(255))
    created_at = Column(DateTime)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")

class TransactionCategory(Base):
    __tablename__ = 'Transaction_Categories'
    
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(30), nullable=False)
    category_code = Column(String(30), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="category")

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
    created_at = Column(DateTime)
    
    # Foreign Keys
    category_id = Column(Integer, ForeignKey('Transaction_Categories.category_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('Momo_User.user_id'), nullable=False)
    
    # Relationships
    category = relationship("TransactionCategory", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    fees = relationship("TransactionFee", back_populates="transaction")
