from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    
    groups = relationship('Group', secondary='groups_users', back_populates='users')

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    users = relationship('User', secondary='groups_users', back_populates='groups')
    records = relationship('Record', back_populates='group')

class GroupUser(Base):
    __tablename__ = 'groups_users'
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)
    comment = Column(String, nullable=True)
    
    group = relationship('Group', back_populates='records')
    loans = relationship('Loan', back_populates='record')

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey('records.id'), nullable=False)
    lender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    borrower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    category = Column(String, nullable=True)
    
    record = relationship('Record', back_populates='loans')
    lender = relationship('User', foreign_keys=[lender_id])
    borrower = relationship('User', foreign_keys=[borrower_id])
