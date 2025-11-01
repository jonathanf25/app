from __future__ import annotations

from functools import lru_cache

from fastapi import Depends

from .schemas.models import BotIntent, User, WhatsAppTemplate
from .services.bots import BotOrchestrator
from .services.distribution import TicketDistributor
from .services.observability import ObservabilityCenter
from .services.security import AuditTrail, RBACGuard
from .services.whatsapp import WhatsAppGateway
from .utils.storage import InMemoryRepository, MultiTenantRepository


department_repo = InMemoryRepository()
user_repo = InMemoryRepository()
ticket_repo = InMemoryRepository()
message_repo = InMemoryRepository()
macro_repo = InMemoryRepository()
template_repo = InMemoryRepository()
audit_trail = AuditTrail()
observability_center = ObservabilityCenter()
distributor = TicketDistributor()
intent_repo = InMemoryRepository()
session_repo = MultiTenantRepository()
whatsapp_gateway = WhatsAppGateway()


@lru_cache
def bot_orchestrator() -> BotOrchestrator:
    intents = [intent_repo.get(intent_id) for intent_id in intent_repo.ids()]
    intents = [intent for intent in intents if isinstance(intent, BotIntent)]
    return BotOrchestrator(intents)


def get_department_repo() -> InMemoryRepository:
    return department_repo


def get_user_repo() -> InMemoryRepository:
    return user_repo


def get_ticket_repo() -> InMemoryRepository:
    return ticket_repo


def get_message_repo() -> InMemoryRepository:
    return message_repo


def get_macro_repo() -> InMemoryRepository:
    return macro_repo


def get_template_repo() -> InMemoryRepository:
    return template_repo


def get_intent_repo() -> InMemoryRepository:
    return intent_repo


def get_audit_trail() -> AuditTrail:
    return audit_trail


def get_observability_center() -> ObservabilityCenter:
    return observability_center


def get_distributor() -> TicketDistributor:
    return distributor


def get_whatsapp_gateway() -> WhatsAppGateway:
    # Mantém gateway com templates sincronizados com o repositório
    whatsapp_gateway.templates = {
        template.id: template for template in template_repo.list() if isinstance(template, WhatsAppTemplate)
    }
    return whatsapp_gateway


def get_rbac_guard(
    user_id: str,
    user_repository: InMemoryRepository = Depends(get_user_repo),
) -> RBACGuard:
    users = [user_repository.get(user_id) for user_id in user_repository.ids()]
    users = [user for user in users if isinstance(user, User)]
    return RBACGuard(users)


def get_session_repo() -> MultiTenantRepository:
    return session_repo
