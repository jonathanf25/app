from __future__ import annotations

from typing import Iterable

from ..schemas.models import Message, WhatsAppTemplate


class WhatsAppGateway:
    """Simula a integração com a WhatsApp Business Platform."""

    def __init__(self, templates: Iterable[WhatsAppTemplate] | None = None) -> None:
        self.templates = {template.id: template for template in templates or []}
        self.sent_messages: list[Message] = []

    def register_template(self, template: WhatsAppTemplate) -> None:
        self.templates[template.id] = template

    def list_templates(self) -> list[WhatsAppTemplate]:
        return list(self.templates.values())

    def send_message(self, message: Message) -> Message:
        self.sent_messages.append(message)
        return message
