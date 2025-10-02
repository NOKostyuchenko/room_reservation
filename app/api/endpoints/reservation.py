from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.reservation import ReservationCreate, ReservationDB
from core.db import get_async_session
from api.validators import check_meeting_room_exists, check_reservation_intersections
from crud.reservation import reservation_crud

router = APIRouter()


@router.post("/", response_model=ReservationDB)
async def create_reservation(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(
        reservation.meetingroom_id, session
    )
    await check_reservation_intersections(
        **reservation.model_dump(),
        session=session
    )
    new_reservation = await reservation_crud.create(
        reservation, session
    )
    return new_reservation