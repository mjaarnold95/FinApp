from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..core.database import get_session
from ..models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    """Get all users"""
    users = session.exec(select(User)).all()
    return users


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a specific user"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    """Create a new user"""
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: User, session: Session = Depends(get_session)):
    """Update a user"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = user_data.model_dump(exclude_unset=True)
    for key, value in user_dict.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Delete a user"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
