from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from models.ration_input_model import RationInput
from models.distribution_model import Distribution
from models.ration_stock_model import RationStock

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_total_inputs_month(self) -> dict:
        current_date = datetime.now()
        
        total_amount = self.db.query(
            func.sum(RationInput.amount).label('total_amount')
        ).filter(
            extract('month', RationInput.date) == current_date.month,
            extract('year', RationInput.date) == current_date.year
        ).scalar()

        return {
            "total_amount": total_amount or 0,
            "month": current_date.month,
            "year": current_date.year
        }
    
    def get_total_distributions_month(self) -> dict:
        current_date = datetime.now()
        
        total_amount = self.db.query(
            func.sum(Distribution.amount).label('total_amount')
        ).filter(
            extract('month', Distribution.date) == current_date.month,
            extract('year', Distribution.date) == current_date.year
        ).scalar()

        return {
            "total_amount": total_amount or 0,
            "month": current_date.month,
            "year": current_date.year
        }
    
    def get_current_total_stock(self) -> dict:
        total_inputs = self.db.query(
            func.sum(RationInput.amount).label('total_inputs')
        ).scalar()

        total_distributions = self.db.query(
            func.sum(Distribution.amount).label('total_distributions')
        ).scalar()

        current_stock = (total_inputs or 0) - (total_distributions or 0)

        return {
            "current_stock": current_stock,
            "total_inputs": total_inputs or 0,
            "total_distributions": total_distributions or 0,
            "last_updated": datetime.now()
        }
    
    def get_current_total_stock(self) -> dict:
        total_stock = self.db.query(
            func.sum(RationStock.stock).label('total_stock')
        ).scalar()

        return {
            "current_stock": total_stock or 0,
            "last_updated": datetime.now()
        }