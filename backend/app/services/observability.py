from __future__ import annotations

from datetime import datetime
from typing import Iterable

from ..schemas.models import ObservabilityProbe


class ObservabilityCenter:
    def __init__(self, probes: Iterable[ObservabilityProbe] | None = None) -> None:
        self._probes = list(probes or [])

    def register_probe(self, name: str, details: str | None = None) -> ObservabilityProbe:
        probe = ObservabilityProbe(name=name, status="ok", last_check=datetime.utcnow(), details=details)
        self._probes.append(probe)
        return probe

    def heartbeat(self, name: str, status: str, details: str | None = None) -> ObservabilityProbe:
        probe = ObservabilityProbe(name=name, status=status, last_check=datetime.utcnow(), details=details)
        self._probes.append(probe)
        return probe

    def list(self) -> list[ObservabilityProbe]:
        return list(self._probes)
