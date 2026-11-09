import database
from services import transaction_audit
from models.distribution_model import Distribution
from services.stock_movements import adjust_stock, require_beneficiary


async def get_all_distribution_service(skip=0, limit=1000, beneficiary_id=None):
    with database.SessionLocal() as db:
        query = db.query(Distribution).filter(Distribution.old == False)
        if beneficiary_id is not None:
            query = query.filter(Distribution.beneficiary_id == beneficiary_id)
        return query.order_by(Distribution.id).offset(skip).limit(limit).all(), query.count()


async def get_distribution_by_id_service(distribution_id):
    with database.SessionLocal() as db:
        return db.query(Distribution).filter(
            Distribution.id == distribution_id, Distribution.old == False
        ).first()


async def create_distribution_service(distribution_dto, actor=None, request=None):
    with database.SessionLocal() as db:
        require_beneficiary(db, distribution_dto.beneficiary_id)
        adjust_stock(db, {distribution_dto.ration_id: -distribution_dto.amount})
        record = Distribution(**distribution_dto.model_dump())
        db.add(record)
        transaction_audit.record_change(db, "CREATE", record, actor, request, distribution_dto.model_dump(exclude_unset=True).keys())
        db.commit()
        db.refresh(record)
        return record


async def update_distribution_service(distribution_dto, actor=None, request=None):
    with database.SessionLocal() as db:
        record = db.query(Distribution).filter(
            Distribution.id == distribution_dto.id, Distribution.old == False
        ).with_for_update().first()
        if record is None:
            return None
        require_beneficiary(db, distribution_dto.beneficiary_id)
        deltas = {record.ration_id: record.amount}
        new_id = distribution_dto.ration_id
        deltas[new_id] = deltas.get(new_id, 0) - distribution_dto.amount
        adjust_stock(db, deltas)
        for key, value in distribution_dto.model_dump(exclude={'id'}, exclude_unset=True).items():
            setattr(record, key, value)
        transaction_audit.record_change(db, "UPDATE", record, actor, request, distribution_dto.model_dump(exclude_unset=True).keys())
        db.commit()
        db.refresh(record)
        return record


async def delete_distribution_service(distribution_id, actor=None, request=None):
    with database.SessionLocal() as db:
        record = db.query(Distribution).filter(
            Distribution.id == distribution_id, Distribution.old == False
        ).with_for_update().first()
        if record is None:
            return False
        adjust_stock(db, {record.ration_id: record.amount})
        db.delete(record)
        transaction_audit.record_change(db, "DELETE", record, actor, request, ())
        db.commit()
        return True
