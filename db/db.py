from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User, Group, GroupUser, Record, Loan

DB_PATH = 'sqlite:///expenso.db'
engine = create_engine(DB_PATH, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
