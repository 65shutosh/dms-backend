from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.models.user import User
from app.schemas.user import UserCreate
from app.core.auth import hash_password

class UserRepository:
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    

    @staticmethod
    async def create(db: AsyncSession, user_data: UserCreate) -> User:
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            role="customer",  # default role
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user