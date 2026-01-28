from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Post
from src.database.models import User


async def create_post(
    session: AsyncSession,
    title: str,
    description: str,
    user_id: int,
) -> Post:
    post = Post(
        title=title,
        description=description,
        user_id=user_id,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

 


async def get_posts_by_user(
    session: AsyncSession,
    user_id: int,
) -> list[Post]:
    result = await session.execute(select(Post).where(Post.user_id == user_id))
    return list(result.scalars().all())
