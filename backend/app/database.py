from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace these with your actual MySQL credentials
DB_USER = "root"
DB_PASSWORD = "Neha@2004"
DB_HOST = "localhost"
DB_NAME = "lambda_functions"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:Neha%402004@localhost/lambda_functions"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
