from __future__ import annotations

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.models import MessageDirection, TicketStatus, UserRole

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_department_and_user() -> None:
    department = {"id": "support", "name": "Suporte", "sla_minutes": 30}
    client.post("/departments", json=department)

    user = {
        "id": "agent-1",
        "name": "Alice",
        "role": UserRole.AGENT.value,
        "department_id": "support",
    }
    response = client.post("/users", json=user)
    assert response.status_code == 201
    assert response.json()["id"] == "agent-1"


def test_ticket_lifecycle() -> None:
    ticket = {
        "id": "ticket-1",
        "department_id": "support",
        "requester": "cliente@example.com",
        "status": TicketStatus.OPEN.value,
        "channel": "whatsapp",
    }
    created = client.post("/tickets", json=ticket)
    assert created.status_code == 201
    assert created.json()["assigned_to"] in (None, "agent-1")

    message = {
        "id": "msg-1",
        "ticket_id": "ticket-1",
        "author_id": "cliente",
        "direction": MessageDirection.INBOUND.value,
        "body": "Olá, preciso de ajuda",
        "channel": "whatsapp",
    }
    added = client.post("/tickets/ticket-1/messages", json=message)
    assert added.status_code == 201

    update = client.patch("/tickets/ticket-1", json={"status": TicketStatus.RESOLVED.value})
    assert update.status_code == 200
    assert update.json()["status"] == TicketStatus.RESOLVED


def test_register_bot_intent() -> None:
    intent = {
        "id": "faq",
        "name": "FAQ",
        "confidence_threshold": 0.1,
        "samples": ["faq", "pergunta"],
    }
    response = client.post("/intents", json=intent)
    assert response.status_code == 201


def test_reporting_dashboard() -> None:
    response = client.get("/reporting/dashboard")
    assert response.status_code == 200
    body = response.json()
    assert any(metric["name"] == "tickets_total" for metric in body)


def test_whatsapp_template_and_message() -> None:
    template = {
        "id": "welcome",
        "name": "Welcome",
        "language": "pt_BR",
        "category": "utility",
        "body": "Olá {{1}}",
    }
    created_template = client.post("/whatsapp/templates", json=template)
    assert created_template.status_code == 201

    outbound = {
        "id": "msg-2",
        "ticket_id": "ticket-1",
        "author_id": "agent-1",
        "direction": MessageDirection.OUTBOUND.value,
        "body": "Olá, posso ajudar?",
        "channel": "whatsapp",
    }
    response = client.post("/whatsapp/messages", json=outbound)
    assert response.status_code == 202
