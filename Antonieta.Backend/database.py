from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base


# Load environment variables
load_dotenv()

# Database connection URL from environment variable
DATABASE_URL = getenv('DATABASE_URL', '')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create tables
def create_tables():
    from models.beneficiary_model import Base as BeneficiaryBase
    from models.ration_stock_model import Base as RationStockBase
    from models.distribution_model import Base as DistributionBase
    
    BeneficiaryBase.metadata.create_all(bind=engine)
    RationStockBase.metadata.create_all(bind=engine)
    DistributionBase.metadata.create_all(bind=engine)

