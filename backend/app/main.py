from __future__ import annotations

from fastapi import FastAPI

from .routers import admin, departments, intents, macros, observability, reporting, tickets, users, whatsapp

app = FastAPI(title="Omnichannel Support Platform", version="0.1.0")

app.include_router(departments.router)
app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(macros.router)
app.include_router(intents.router)
app.include_router(whatsapp.router)
app.include_router(admin.router)
app.include_router(reporting.router)
app.include_router(observability.router)


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
