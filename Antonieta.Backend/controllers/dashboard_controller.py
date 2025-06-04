from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.dashboard_service import DashboardService
from typing import List

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/total-inputs-month")
async def get_total_inputs_month(db: Session = Depends(get_db)):
    try:
        dashboard_service = DashboardService(db)
        return dashboard_service.get_total_inputs_month()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/total-distributions-month")
async def get_total_distributions_month(db: Session = Depends(get_db)):
    try:
        dashboard_service = DashboardService(db)
        return dashboard_service.get_total_distributions_month()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/current-total-stock")
async def get_current_total_stock(db: Session = Depends(get_db)):
    try:
        dashboard_service = DashboardService(db)
        return dashboard_service.get_current_total_stock()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/beneficiaries-dashboard")
async def get_beneficiaries_dashboard(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """
    Retorna dados consolidados dos beneficiários para o dashboard
    
    Args:
        skip: Número de registros para pular (offset)
        limit: Número máximo de registros para retornar
    """
    try:
        dashboard_service = DashboardService(db)
        data, total = dashboard_service.get_beneficiaries_dashboard(skip=skip, limit=limit)
        return {
            "data": data,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))