from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ..deps import get_audit_trail
from ..schemas.models import AuditLog
from ..services.security import AuditTrail

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/audits", response_model=list[AuditLog])
def list_audits(trail: AuditTrail = Depends(get_audit_trail)) -> list[AuditLog]:
    return trail.list()


@router.post("/audits", response_model=AuditLog, status_code=status.HTTP_201_CREATED)
def record_audit(entry: AuditLog, trail: AuditTrail = Depends(get_audit_trail)) -> AuditLog:
    trail.record(entry)
    return entry
