from __future__ import annotations

from typing import Iterable

from fastapi import HTTPException, status

from ..schemas.models import AuditLog, User, UserRole


class RBACGuard:
    def __init__(self, users: Iterable[User]) -> None:
        self._users = {user.id: user for user in users}

    def require_role(self, user_id: str, allowed_roles: list[UserRole]) -> None:
        user = self._users.get(user_id)
        if not user or user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")


class AuditTrail:
    def __init__(self) -> None:
        self._entries: list[AuditLog] = []

    def record(self, entry: AuditLog) -> None:
        self._entries.append(entry)

    def list(self) -> list[AuditLog]:
        return list(self._entries)
