from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from typing import List, Tuple

from models.ration_input_model import RationInput
from models.distribution_model import Distribution
from models.ration_stock_model import RationStock
from models.beneficiary_model import Beneficiary

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
    
    def get_beneficiaries_dashboard(self, skip: int = 0, limit: int = 10) -> Tuple[List[dict], int]:
        """
        Retorna dados consolidados dos beneficiários para o dashboard
        contendo total recebido no mês para cada beneficiário.

        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros para retornar

        Returns:
            Tupla contendo a lista de beneficiários e o total de registros
        """
        current_date = datetime.now()

        # Busca total de beneficiários
        total = self.db.query(func.count(Beneficiary.id)).scalar()

        # Busca beneficiários com paginação
        beneficiaries = self.db.query(Beneficiary).offset(skip).limit(limit).all()

        dashboard_data = []

        for beneficiary in beneficiaries:
            # Calcula total recebido no mês
            received_amount = self.db.query(
                func.sum(Distribution.amount).label('total_received')
            ).filter(
                Distribution.beneficiary_id == beneficiary.id,
                extract('month', Distribution.date) == current_date.month,
                extract('year', Distribution.date) == current_date.year
            ).scalar() or 0

            dashboard_data.append({
                "id": beneficiary.id,
                "nome": beneficiary.name,
                "recebido_mes": received_amount
            })

        return dashboard_data, total
