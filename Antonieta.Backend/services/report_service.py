from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from models.distribution_model import Distribution
from models.ration_stock_model import RationStock
from models.beneficiary_model import Beneficiary


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_distribution_volume_by_month(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        ration_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        beneficiary_id: Optional[int] = None
    ) -> Dict:
        """
        Retorna o volume de ração distribuído consolidado por mês.
        
        Args:
            year: Ano para filtrar distribuições (if month is not specified, all months of the year)
            month: Mês específico para filtrar distribuições (1-12)
            ration_id: ID do tipo de ração para filtrar
            start_date: Data inicial no formato 'YYYY-MM-DD'
            end_date: Data final no formato 'YYYY-MM-DD'
            beneficiary_id: ID do beneficiário para filtrar
            
        Returns:
            Dicionário com dados consolidados de distribuição por mês
        """
        query = self.db.query(
            extract('year', Distribution.date).label('year'),
            extract('month', Distribution.date).label('month'),
            Distribution.ration_id,
            RationStock.name.label('ration_name'),
            RationStock.unit,
            func.sum(Distribution.amount).label('total_volume'),
            func.count(Distribution.id).label('distribution_count')
        ).join(
            RationStock, Distribution.ration_id == RationStock.id
        ).filter(
            Distribution.old == False
        )

        # Aplicar filtros - prioridade para start_date/end_date
        if start_date is not None or end_date is not None:
            # Se range de datas foi especificado, usar apenas isso
            if start_date is not None:
                try:
                    start = datetime.strptime(start_date, '%Y-%m-%d')
                    query = query.filter(Distribution.date >= start)
                except ValueError:
                    raise ValueError(f"Formato de data inválido para start_date: {start_date}. Use 'YYYY-MM-DD'")
            
            if end_date is not None:
                try:
                    end = datetime.strptime(end_date, '%Y-%m-%d')
                    # Adiciona um dia para incluir todo o dia final
                    end = end + timedelta(days=1)
                    query = query.filter(Distribution.date < end)
                except ValueError:
                    raise ValueError(f"Formato de data inválido para end_date: {end_date}. Use 'YYYY-MM-DD'")
        else:
            # Se nenhum range de datas, usar year e month
            if year is not None and month is None:
                query = query.filter(extract('year', Distribution.date) == year)
            
            if month is not None:
                query = query.filter(extract('month', Distribution.date) == month)
                if year is None:
                    # Se especificar mês sem ano, assume o ano atual
                    year = datetime.now().year
                    query = query.filter(extract('year', Distribution.date) == year)
                else:
                    query = query.filter(extract('year', Distribution.date) == year)
        
        if ration_id is not None:
            query = query.filter(Distribution.ration_id == ration_id)
        
        if beneficiary_id is not None:
            query = query.filter(Distribution.beneficiary_id == beneficiary_id)

        
        query = query.group_by(
            extract('year', Distribution.date),
            extract('month', Distribution.date),
            Distribution.ration_id,
            RationStock.name,
            RationStock.unit
        ).order_by(
            extract('year', Distribution.date).desc(),
            extract('month', Distribution.date).desc(),
            RationStock.name
        )

        results = query.all()

        # Consolidar dados
        data_by_month = {}
        total_volume = 0
        total_distributions = 0

        for row in results:
            month_key = f"{int(row.year):04d}-{int(row.month):02d}"
            
            if month_key not in data_by_month:
                data_by_month[month_key] = {
                    "year": int(row.year),
                    "month": int(row.month),
                    "month_year": month_key,
                    "rations": [],
                    "total_volume_month": 0,
                    "total_distributions_month": 0
                }
            
            ration_info = {
                "ration_id": row.ration_id,
                "ration_name": row.ration_name,
                "unit": row.unit,
                "volume": float(row.total_volume) if row.total_volume else 0,
                "distribution_count": row.distribution_count
            }
            
            data_by_month[month_key]["rations"].append(ration_info)
            data_by_month[month_key]["total_volume_month"] += float(row.total_volume) if row.total_volume else 0
            data_by_month[month_key]["total_distributions_month"] += row.distribution_count
            
            total_volume += float(row.total_volume) if row.total_volume else 0
            total_distributions += row.distribution_count

        return {
            "filters_applied": {
                "year": year,
                "month": month,
                "ration_id": ration_id,
                "start_date": start_date,
                "end_date": end_date,
                "beneficiary_id": beneficiary_id
            },
            "summary": {
                "total_volume": total_volume,
                "total_distributions": total_distributions,
                "periods_count": len(data_by_month)
            },
            "data": list(data_by_month.values())
        }

    def get_distribution_summary_by_ration(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Retorna um resumo de distribuição agrupado por tipo de ração.
        
        Args:
            year: Ano para filtrar distribuições
            month: Mês específico para filtrar distribuições
            start_date: Data inicial no formato 'YYYY-MM-DD'
            end_date: Data final no formato 'YYYY-MM-DD'
            
        Returns:
            Dicionário com dados consolidados de distribuição por tipo de ração
        """
        query = self.db.query(
            Distribution.ration_id,
            RationStock.name.label('ration_name'),
            RationStock.unit,
            func.sum(Distribution.amount).label('total_volume'),
            func.count(Distribution.id).label('distribution_count'),
            func.count(func.distinct(Distribution.beneficiary_id)).label('unique_beneficiaries')
        ).join(
            RationStock, Distribution.ration_id == RationStock.id
        ).filter(
            Distribution.old == False
        )

        # Aplicar filtros - prioridade para start_date/end_date
        if start_date is not None or end_date is not None:
            # Se range de datas foi especificado, usar apenas isso
            if start_date is not None:
                try:
                    start = datetime.strptime(start_date, '%Y-%m-%d')
                    query = query.filter(Distribution.date >= start)
                except ValueError:
                    raise ValueError(f"Formato de data inválido para start_date: {start_date}. Use 'YYYY-MM-DD'")
            
            if end_date is not None:
                try:
                    end = datetime.strptime(end_date, '%Y-%m-%d')
                    end = end + timedelta(days=1)
                    query = query.filter(Distribution.date < end)
                except ValueError:
                    raise ValueError(f"Formato de data inválido para end_date: {end_date}. Use 'YYYY-MM-DD'")
        else:
            # Se nenhum range de datas, usar year e month
            if year is not None:
                query = query.filter(extract('year', Distribution.date) == year)
            
            if month is not None:
                query = query.filter(extract('month', Distribution.date) == month)


        query = query.group_by(
            Distribution.ration_id,
            RationStock.name,
            RationStock.unit
        ).order_by(
            func.sum(Distribution.amount).desc()
        )

        results = query.all()

        rations = []
        total_volume = 0
        total_distributions = 0

        for row in results:
            ration_info = {
                "ration_id": row.ration_id,
                "ration_name": row.ration_name,
                "unit": row.unit,
                "total_volume": float(row.total_volume) if row.total_volume else 0,
                "distribution_count": row.distribution_count,
                "unique_beneficiaries": row.unique_beneficiaries
            }
            rations.append(ration_info)
            total_volume += float(row.total_volume) if row.total_volume else 0
            total_distributions += row.distribution_count

        return {
            "filters_applied": {
                "year": year,
                "month": month,
                "start_date": start_date,
                "end_date": end_date
            },
            "summary": {
                "total_volume": total_volume,
                "total_distributions": total_distributions,
                "unique_rations": len(rations)
            },
            "data": rations
        }
