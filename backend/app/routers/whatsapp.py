from __future__ import annotations

from fastapi import APIRouter, Depends, status

from ..deps import get_session_repo, get_template_repo, get_whatsapp_gateway
from ..schemas.models import Message, WhatsAppTemplate
from ..services.whatsapp import WhatsAppGateway
from ..utils.storage import InMemoryRepository, MultiTenantRepository

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


@router.get("/templates", response_model=list[WhatsAppTemplate])
def list_templates(repo: InMemoryRepository = Depends(get_template_repo)) -> list[WhatsAppTemplate]:
    return [template for template in repo.list() if isinstance(template, WhatsAppTemplate)]


@router.post("/templates", response_model=WhatsAppTemplate, status_code=status.HTTP_201_CREATED)
def register_template(
    template: WhatsAppTemplate,
    gateway: WhatsAppGateway = Depends(get_whatsapp_gateway),
    repo: InMemoryRepository = Depends(get_template_repo),
) -> WhatsAppTemplate:
    gateway.register_template(template)
    repo.upsert(template)
    return template


@router.post("/messages", response_model=Message, status_code=status.HTTP_202_ACCEPTED)
def send_message(
    message: Message,
    gateway: WhatsAppGateway = Depends(get_whatsapp_gateway),
    sessions: MultiTenantRepository = Depends(get_session_repo),
) -> Message:
    session = sessions.for_tenant(message.ticket_id)
    session.upsert(message)
    return gateway.send_message(message)
