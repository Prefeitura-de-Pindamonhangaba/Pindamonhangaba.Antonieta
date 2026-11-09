from sqlalchemy import func
import database
from services import transaction_audit
from models.ration_input_model import RationInput
from services.stock_movements import adjust_stock


async def get_all_ration_input_service(skip=0, limit=1000, stock_id=None):
    with database.SessionLocal() as db:
        query = db.query(RationInput)
        if stock_id is not None:
            query = query.filter(RationInput.ration_stock_id == stock_id)
        return query.order_by(RationInput.id).offset(skip).limit(limit).all(), query.count()


async def get_ration_input_by_id_service(ration_input_id):
    with database.SessionLocal() as db:
        return db.get(RationInput, ration_input_id)


async def create_ration_input_service(ration_input_dto, actor=None, request=None):
    with database.SessionLocal() as db:
        adjust_stock(db, {ration_input_dto.ration_stock_id: ration_input_dto.amount})
        record = RationInput(**ration_input_dto.model_dump())
        db.add(record)
        transaction_audit.record_change(db, "CREATE", record, actor, request, ration_input_dto.model_dump(exclude_unset=True).keys())
        db.commit()
        db.refresh(record)
        return record


async def update_ration_input_service(ration_input_dto, actor=None, request=None):
    with database.SessionLocal() as db:
        record = db.query(RationInput).filter(
            RationInput.id == ration_input_dto.id
        ).with_for_update().first()
        if record is None:
            return None
        deltas = {record.ration_stock_id: -record.amount}
        new_id = ration_input_dto.ration_stock_id
        deltas[new_id] = deltas.get(new_id, 0) + ration_input_dto.amount
        adjust_stock(db, deltas)
        for key, value in ration_input_dto.model_dump(exclude={'id'}).items():
            setattr(record, key, value)
        transaction_audit.record_change(db, "UPDATE", record, actor, request, ration_input_dto.model_dump(exclude_unset=True).keys())
        db.commit()
        db.refresh(record)
        return record


async def delete_ration_input_service(ration_input_id, actor=None, request=None):
    with database.SessionLocal() as db:
        record = db.query(RationInput).filter(
            RationInput.id == ration_input_id
        ).with_for_update().first()
        if record is None:
            return False
        adjust_stock(db, {record.ration_stock_id: -record.amount})
        db.delete(record)
        transaction_audit.record_change(db, "DELETE", record, actor, request, ())
        db.commit()
        return True
