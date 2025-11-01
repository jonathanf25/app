from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Channel(str, Enum):
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    CHAT = "chat"


class Department(BaseModel):
    id: str = Field(description="Identificador único do departamento")
    name: str = Field(description="Nome do departamento")
    sla_minutes: int = Field(default=60, description="SLA de atendimento em minutos")
    description: Optional[str] = Field(default=None, description="Descrição do escopo do departamento")


class UserRole(str, Enum):
    AGENT = "agent"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"
    BOT = "bot"


class User(BaseModel):
    id: str
    name: str
    role: UserRole
    department_id: Optional[str] = None
    active: bool = True


class TicketStatus(str, Enum):
    OPEN = "open"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Ticket(BaseModel):
    id: str
    department_id: str
    requester: str
    status: TicketStatus = TicketStatus.OPEN
    channel: Channel = Channel.WHATSAPP
    assigned_to: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)


class MessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Message(BaseModel):
    id: str
    ticket_id: str
    author_id: str
    direction: MessageDirection
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    channel: Channel = Channel.WHATSAPP
    attachments: list[str] = Field(default_factory=list)


class Macro(BaseModel):
    id: str
    title: str
    content: str
    department_id: Optional[str] = None


class BotIntent(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    confidence_threshold: float = 0.6
    samples: list[str] = Field(default_factory=list)
    department_id: Optional[str] = None


class WhatsAppTemplate(BaseModel):
    id: str
    name: str
    language: str
    category: str
    body: str


class AuditLog(BaseModel):
    id: str
    actor_id: str
    action: str
    payload: dict
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DashboardMetric(BaseModel):
    name: str
    value: float
    unit: str = "count"
    description: Optional[str] = None


class IntegrationConfig(BaseModel):
    name: str
    enabled: bool
    settings: dict = Field(default_factory=dict)


class ObservabilityProbe(BaseModel):
    name: str
    status: str
    last_check: datetime
    details: Optional[str] = None
