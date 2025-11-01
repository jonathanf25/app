from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..deps import get_distributor, get_user_repo
from ..schemas.models import User, UserRole
from ..services.distribution import TicketDistributor
from ..utils.storage import InMemoryRepository

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[User])
def list_users(
    role: UserRole | None = Query(default=None),
    repo: InMemoryRepository = Depends(get_user_repo),
) -> list[User]:
    users = [user for user in repo.list() if isinstance(user, User)]
    if role:
        users = [user for user in users if user.role == role]
    return users


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: User,
    repo: InMemoryRepository = Depends(get_user_repo),
    distributor: TicketDistributor = Depends(get_distributor),
) -> User:
    repo.upsert(user)
    if user.role == UserRole.AGENT and user.department_id:
        distributor.queue.register_agent(user.department_id, user.id)
    return user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str, repo: InMemoryRepository = Depends(get_user_repo)) -> User:
    user = repo.get(user_id)
    if not isinstance(user, User):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user
