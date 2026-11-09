from models.audit_log_model import AuditLog


def record_change(db, action, record, actor=None, request=None, fields=()):
    """Persist operation metadata in the same transaction, without personal values."""
    if actor is None:
        return
    if action == "CREATE":
        record.created_by = actor.id
    elif action == "UPDATE":
        record.updated_by = actor.id
    db.flush()
    db.add(AuditLog(
        user_id=actor.id, user_email=actor.email,
        action=action, entity_type=type(record).__name__, entity_id=record.id,
        description=f"{type(record).__name__} {action}",
        changes={"fields": sorted(fields)},
        ip_address=request.client.host if request and request.client else None,
        user_agent=request.headers.get("user-agent") if request else None,
    ))
