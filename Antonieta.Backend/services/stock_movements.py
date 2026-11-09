from fastapi import HTTPException
from models.ration_stock_model import RationStock
from models.beneficiary_model import Beneficiary


def adjust_stock(db, deltas):
    """Lock all involved stocks in ID order; validate before applying any change."""
    stocks = db.query(RationStock).filter(
        RationStock.id.in_(deltas)
    ).order_by(RationStock.id).with_for_update().all()
    if len(stocks) != len(deltas):
        raise HTTPException(status_code=404, detail="Ração não encontrada")
    for stock in stocks:
        if stock.stock + deltas[stock.id] < 0:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
    for stock in stocks:
        stock.stock += deltas[stock.id]


def require_beneficiary(db, beneficiary_id):
    if not db.query(Beneficiary).filter(
        Beneficiary.id == beneficiary_id, Beneficiary.old == False
    ).first():
        raise HTTPException(status_code=404, detail="Beneficiário não encontrado")
