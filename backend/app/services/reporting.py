from __future__ import annotations

from collections import Counter
from datetime import datetime
from typing import Iterable

from ..schemas.models import DashboardMetric, Ticket


class ReportingService:
    def __init__(self, tickets: Iterable[Ticket]) -> None:
        self._tickets = list(tickets)

    def generate_dashboard(self) -> list[DashboardMetric]:
        total = len(self._tickets)
        by_status = Counter(ticket.status for ticket in self._tickets)
        now = datetime.utcnow().isoformat()
        metrics = [
            DashboardMetric(name="tickets_total", value=float(total), description=f"Total de tickets em {now}"),
        ]
        metrics.extend(
            DashboardMetric(name=f"tickets_{status.value}", value=float(count), description="Quantidade por status")
            for status, count in by_status.items()
        )
        return metrics
