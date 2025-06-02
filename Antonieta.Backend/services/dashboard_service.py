from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from models.ration_input_model import RationInput
from models.distribution_model import Distribution

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