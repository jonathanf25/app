from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..deps import get_macro_repo
from ..schemas.models import Macro
from ..utils.storage import InMemoryRepository

router = APIRouter(prefix="/macros", tags=["macros"])


@router.get("", response_model=list[Macro])
def list_macros(repo: InMemoryRepository = Depends(get_macro_repo)) -> list[Macro]:
    return [macro for macro in repo.list() if isinstance(macro, Macro)]


@router.post("", response_model=Macro, status_code=status.HTTP_201_CREATED)
def create_macro(macro: Macro, repo: InMemoryRepository = Depends(get_macro_repo)) -> Macro:
    repo.upsert(macro)
    return macro


@router.delete("/{macro_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_macro(macro_id: str, repo: InMemoryRepository = Depends(get_macro_repo)) -> None:
    macro = repo.get(macro_id)
    if not isinstance(macro, Macro):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Macro não encontrada")
    repo.delete(macro_id)
