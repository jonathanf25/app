from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..deps import bot_orchestrator, get_distributor, get_message_repo, get_ticket_repo
from ..schemas.models import Message, MessageDirection, Ticket, TicketStatus
from ..services.bots import BotOrchestrator
from ..services.distribution import TicketDistributor
from ..utils.storage import InMemoryRepository

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=list[Ticket])
def list_tickets(
    status_filter: TicketStatus | None = Query(default=None),
    repo: InMemoryRepository = Depends(get_ticket_repo),
) -> list[Ticket]:
    tickets = [ticket for ticket in repo.list() if isinstance(ticket, Ticket)]
    if status_filter:
        tickets = [ticket for ticket in tickets if ticket.status == status_filter]
    return tickets


@router.post("", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: Ticket,
    ticket_repo: InMemoryRepository = Depends(get_ticket_repo),
    distributor: TicketDistributor = Depends(get_distributor),
) -> Ticket:
    ticket.created_at = datetime.utcnow()
    ticket.updated_at = ticket.created_at
    assigned = distributor.assign_ticket(ticket)
    ticket_repo.upsert(assigned)
    return assigned


@router.post("/{ticket_id}/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
def add_message(
    ticket_id: str,
    message: Message,
    ticket_repo: InMemoryRepository = Depends(get_ticket_repo),
    message_repo: InMemoryRepository = Depends(get_message_repo),
    orchestrator: BotOrchestrator = Depends(bot_orchestrator),
) -> Message:
    ticket = ticket_repo.get(ticket_id)
    if not isinstance(ticket, Ticket):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket não encontrado")
    message.ticket_id = ticket_id
    message.created_at = datetime.utcnow()
    message_repo.upsert(message)
    ticket.updated_at = message.created_at
    ticket_repo.upsert(ticket)
    if message.direction == MessageDirection.INBOUND:
        orchestrator.handle_message(message)
    return message


@router.patch("/{ticket_id}", response_model=Ticket)
def update_ticket_status(
    ticket_id: str,
    status_update: dict[str, Any],
    repo: InMemoryRepository = Depends(get_ticket_repo),
) -> Ticket:
    ticket = repo.get(ticket_id)
    if not isinstance(ticket, Ticket):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket não encontrado")
    if "status" in status_update:
        ticket.status = TicketStatus(status_update["status"])
    if "assigned_to" in status_update:
        ticket.assigned_to = status_update["assigned_to"]
    ticket.updated_at = datetime.utcnow()
    repo.upsert(ticket)
    return ticket
