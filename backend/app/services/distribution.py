from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Optional

from ..schemas.models import Ticket


class RoundRobinQueue:
    """Fila simples para distribuição de tickets entre agentes."""

    def __init__(self) -> None:
        self._agents: Deque[str] = deque()
        self._last_assigned: Dict[str, str] = {}

    def register_agent(self, department_id: str, agent_id: str) -> None:
        if agent_id not in self._agents:
            self._agents.append(agent_id)
        self._last_assigned.setdefault(department_id, "")

    def unregister_agent(self, agent_id: str) -> None:
        try:
            self._agents.remove(agent_id)
        except ValueError:
            pass

    def next_agent(self, department_id: str) -> Optional[str]:
        if not self._agents:
            return None
        agent_id = self._agents[0]
        self._agents.rotate(-1)
        self._last_assigned[department_id] = agent_id
        return agent_id


class TicketDistributor:
    def __init__(self, queue: RoundRobinQueue | None = None) -> None:
        self.queue = queue or RoundRobinQueue()

    def assign_ticket(self, ticket: Ticket) -> Ticket:
        agent_id = self.queue.next_agent(ticket.department_id)
        if agent_id:
            ticket.assigned_to = agent_id
        return ticket
