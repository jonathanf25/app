from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ..deps import get_observability_center
from ..schemas.models import ObservabilityProbe
from ..services.observability import ObservabilityCenter

router = APIRouter(prefix="/observability", tags=["observability"])


@router.get("/probes", response_model=list[ObservabilityProbe])
def list_probes(center: ObservabilityCenter = Depends(get_observability_center)) -> list[ObservabilityProbe]:
    return center.list()


@router.post("/probes", response_model=ObservabilityProbe, status_code=status.HTTP_201_CREATED)
def register_probe(
    probe: ObservabilityProbe,
    center: ObservabilityCenter = Depends(get_observability_center),
) -> ObservabilityProbe:
    return center.heartbeat(probe.name, probe.status, probe.details)
