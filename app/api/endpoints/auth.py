from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.db_connect import get_async_session
from schemas.users import UserCreate, UserInBD, Credentials
from models.users import User


router = APIRouter()


@router.post(
    "/signup",
    response_model=UserInBD,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    user_dto = user_create.model_dump()
    user = User(**user_dto)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post(
    "/login",
    response_model=UserInBD,
    status_code=status.HTTP_200_OK
)
async def login(
    credentials: Credentials,
    session: AsyncSession = Depends(get_async_session)
):
    statement = select(User).where(User.login == credentials.login)
    result_request = await session.execute(statement)
    user = result_request.scalar()

    if not user or not user.check_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return user
