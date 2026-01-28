from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.models import User


async def create_user(
    session: AsyncSession,
    name: str,
    email: str,
) -> User:
    user = User(name=name, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)  # loads generated id
    return user


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_with_posts(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    result = await session.execute(
        select(User).options(selectinload(User.posts)).where(User.id == user_id)
    )
    return result.scalar_one_or_none()
