from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection URL from environment variable
DATABASE_URL = getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/notes')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create tables
def create_tables():
    from models.beneficiaries_model import Base as BeneficiarieBase
    from models.distribution_model import Base as DistributionBase
    from models.ration_model import Base as RationBase

    BeneficiarieBase.metadata.create_all(bind=engine)
    DistributionBase.metadata.create_all(bind=engine)
    RationBase.metadata.create_all(bind=engine)
