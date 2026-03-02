from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from services.report_service import ReportService
from typing import Optional

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/distribution-volume-by-month")
async def get_distribution_volume_by_month(
    db: Session = Depends(get_db),
    year: Optional[int] = Query(None, description="Ano para filtrar distribuições"),
    month: Optional[int] = Query(None, description="Mês para filtrar distribuições (1-12)"),
    ration_id: Optional[int] = Query(None, description="ID do tipo de ração para filtrar"),
    beneficiary_id: Optional[int] = Query(None, description="ID do beneficiário para filtrar"),
    start_date: Optional[str] = Query(
        None, 
        description="Data inicial no formato YYYY-MM-DD",
        example="2024-01-01"
    ),
    end_date: Optional[str] = Query(
        None,
        description="Data final no formato YYYY-MM-DD",
        example="2024-12-31"
    )
):
    """
    Retorna o volume de ração distribuído consolidado por mês.
    
    **Query Parameters:**
    - `year`: Filtrar por ano específico (ex: 2024)
    - `month`: Filtrar por mês específico (1-12). Se especificado sem ano, usa o ano atual
    - `ration_id`: Filtrar por ID do tipo de ração
    - `beneficiary_id`: Filtrar por ID do beneficiário
    - `start_date`: Data inicial do período (YYYY-MM-DD)
    - `end_date`: Data final do período (YYYY-MM-DD)
    
    **Exemplos de uso:**
    - `/reports/distribution-volume-by-month?year=2024` - Todas as distribuições do ano 2024
    - `/reports/distribution-volume-by-month?year=2024&month=3` - Distribuições de março de 2024
    - `/reports/distribution-volume-by-month?ration_id=1` - Distribuições de um tipo de ração específico
    - `/reports/distribution-volume-by-month?start_date=2024-01-01&end_date=2024-06-30` - Período customizado
    - `/reports/distribution-volume-by-month?year=2024&ration_id=2&beneficiary_id=5` - Múltiplos filtros combinados
    """
    try:
        # Validação do mês
        if month is not None and (month < 1 or month > 12):
            raise HTTPException(status_code=400, detail="Mês deve estar entre 1 e 12")
        
        report_service = ReportService(db)
        result = report_service.get_distribution_volume_by_month(
            year=year,
            month=month,
            ration_id=ration_id,
            start_date=start_date,
            end_date=end_date,
            beneficiary_id=beneficiary_id
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/distribution-summary-by-ration")
async def get_distribution_summary_by_ration(
    db: Session = Depends(get_db),
    year: Optional[int] = Query(None, description="Ano para filtrar distribuições"),
    month: Optional[int] = Query(None, description="Mês para filtrar distribuições (1-12)"),
    start_date: Optional[str] = Query(
        None,
        description="Data inicial no formato YYYY-MM-DD",
        example="2024-01-01"
    ),
    end_date: Optional[str] = Query(
        None,
        description="Data final no formato YYYY-MM-DD",
        example="2024-12-31"
    )
):
    """
    Retorna um resumo de distribuição agrupado por tipo de ração.
    
    **Query Parameters:**
    - `year`: Filtrar por ano específico (ex: 2024)
    - `month`: Filtrar por mês específico (1-12)
    - `start_date`: Data inicial do período (YYYY-MM-DD)
    - `end_date`: Data final do período (YYYY-MM-DD)
    
    **Exemplos de uso:**
    - `/reports/distribution-summary-by-ration?year=2024` - Resumo anual
    - `/reports/distribution-summary-by-ration?year=2024&month=3` - Resumo do mês de março de 2024
    - `/reports/distribution-summary-by-ration?start_date=2024-01-01&end_date=2024-12-31` - Período customizado
    """
    try:
        # Validação do mês
        if month is not None and (month < 1 or month > 12):
            raise HTTPException(status_code=400, detail="Mês deve estar entre 1 e 12")
        
        report_service = ReportService(db)
        result = report_service.get_distribution_summary_by_ration(
            year=year,
            month=month,
            start_date=start_date,
            end_date=end_date
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
