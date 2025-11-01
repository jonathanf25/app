from __future__ import annotations

from fastapi import APIRouter, Depends

from ..deps import get_ticket_repo
from ..schemas.models import DashboardMetric, Ticket
from ..services.reporting import ReportingService
from ..utils.storage import InMemoryRepository

router = APIRouter(prefix="/reporting", tags=["analytics"])


@router.get("/dashboard", response_model=list[DashboardMetric])
def dashboard(repo: InMemoryRepository = Depends(get_ticket_repo)) -> list[DashboardMetric]:
    tickets = [ticket for ticket in repo.list() if isinstance(ticket, Ticket)]
    service = ReportingService(tickets)
    return service.generate_dashboard()
