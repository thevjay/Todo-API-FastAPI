import os  # Import the os module
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)  # Create a SQLAlchemy engine
# What is an sql alchemy engine?    
# An Engine is a factory for Connection objects. It encapsulates a connection pool 
# that minimizes the cost of connecting to the database by reusing existing connections
# and provides a consistent API for working with transactions.

metadata = MetaData() # Create a SQLALchemy MetaData object

Sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine) # Create a SQLAlchemy sessionmaker object

Base = declarative_base()  # Create a SQLAlchemy declarative base object


1.28