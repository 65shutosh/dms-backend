from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserLogin
from app.core.auth import verify_password, create_access_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserOut

router = APIRouter()

@router.post("/login")
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    # 1. Get user by email via repository
    user = await UserRepository.get_by_email(db, user_credentials.email)

    # 2. If user not found or password mismatch
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # 3. Create token
    access_token = create_access_token(data={"sub": user.email, "role": user.role})

    # 4. Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if user already exists
    existing_user = await UserRepository.get_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Create user
    new_user = await UserRepository.create(db, user_data)

    # 3. Return user (auto-converted by FastAPI using UserOut)
    return new_user