from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.dashboard_service import DashboardService

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