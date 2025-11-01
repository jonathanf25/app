from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, MutableMapping, TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class InMemoryRepository:
    """Repositório genérico em memória baseado em dicionários."""

    def __init__(self) -> None:
        self._items: MutableMapping[str, BaseModel] = {}

    def list(self) -> Iterable[BaseModel]:
        return list(self._items.values())

    def ids(self) -> Iterable[str]:
        return list(self._items.keys())

    def get(self, item_id: str) -> BaseModel | None:
        return self._items.get(item_id)

    def upsert(self, item: T) -> T:
        self._items[item.id] = item
        return item

    def delete(self, item_id: str) -> None:
        self._items.pop(item_id, None)


class MultiTenantRepository:
    """Armazena entidades segmentadas por departamento/tenant."""

    def __init__(self) -> None:
        self._tenants: Dict[str, InMemoryRepository] = defaultdict(InMemoryRepository)

    def for_tenant(self, tenant_id: str) -> InMemoryRepository:
        return self._tenants[tenant_id]

    def tenants(self) -> Iterable[str]:
        return list(self._tenants.keys())
