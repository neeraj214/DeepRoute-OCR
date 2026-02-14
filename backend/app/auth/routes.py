from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import UserCreate, UserRead, Token
from .models import User
from .auth_utils import get_password_hash, verify_password, create_access_token
from .dependencies import get_db, get_current_active_user, TOKEN_BLACKLIST

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead(id=user.id, email=user.email, full_name=user.full_name, role=user.role, is_active=user.is_active)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token_data = create_access_token(subject=user.email, role=user.role)
    return Token(access_token=token_data["access_token"], expires_in=token_data["expires_in"])

@router.post("/logout")
def logout(request: Request, current_user: User = Depends(get_current_active_user)) -> Any:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth.removeprefix("Bearer ").strip()
        if token:
            TOKEN_BLACKLIST.add(token)
            return {"status": "ok", "message": "Token revoked"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing bearer token")
