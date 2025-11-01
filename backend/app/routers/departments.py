from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..deps import get_department_repo
from ..schemas.models import Department
from ..utils.storage import InMemoryRepository

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("", response_model=list[Department])
def list_departments(repo: InMemoryRepository = Depends(get_department_repo)) -> list[Department]:
    return [dept for dept in repo.list() if isinstance(dept, Department)]


@router.post("", response_model=Department, status_code=status.HTTP_201_CREATED)
def create_department(department: Department, repo: InMemoryRepository = Depends(get_department_repo)) -> Department:
    repo.upsert(department)
    return department


@router.get("/{department_id}", response_model=Department)
def get_department(department_id: str, repo: InMemoryRepository = Depends(get_department_repo)) -> Department:
    department = repo.get(department_id)
    if not isinstance(department, Department):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Departamento não encontrado")
    return department
