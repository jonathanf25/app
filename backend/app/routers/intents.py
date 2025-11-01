from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..deps import bot_orchestrator, get_intent_repo
from ..schemas.models import BotIntent
from ..utils.storage import InMemoryRepository

router = APIRouter(prefix="/intents", tags=["bots"])


@router.get("", response_model=list[BotIntent])
def list_intents(repo: InMemoryRepository = Depends(get_intent_repo)) -> list[BotIntent]:
    return [intent for intent in repo.list() if isinstance(intent, BotIntent)]


@router.post("", response_model=BotIntent, status_code=status.HTTP_201_CREATED)
def create_intent(intent: BotIntent, repo: InMemoryRepository = Depends(get_intent_repo)) -> BotIntent:
    repo.upsert(intent)
    bot_orchestrator.cache_clear()  # type: ignore[attr-defined]
    return intent


@router.get("/{intent_id}", response_model=BotIntent)
def get_intent(intent_id: str, repo: InMemoryRepository = Depends(get_intent_repo)) -> BotIntent:
    intent = repo.get(intent_id)
    if not isinstance(intent, BotIntent):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intent não encontrada")
    return intent
