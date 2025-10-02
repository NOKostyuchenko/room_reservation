from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.reservation import (
    ReservationCreate, ReservationDB, ReservationUpdate
)
from core.db import get_async_session
from api.validators import (
    check_meeting_room_exists,
    check_reservation_intersections,
    check_reservation_before_edit
)
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


@router.get(
    "/",
    response_model=list[ReservationDB]
)
async def get_all_reservations(
    session: AsyncSession = Depends(get_async_session)
):
    reserved_rooms: list = await reservation_crud.get_multi(session)
    return reserved_rooms


@router.delete(
    "/{reservation_id}",
    response_model=ReservationDB
)
async def delete_reservation(
    reservation_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(reservation_id, session)
    db_reservation = await reservation_crud.delete(reservation, session)
    return db_reservation


@router.patch(
    "/{reservation_id}",
    response_model=ReservationDB
)
async def update_reservation(
    reservation_id: int,
    update_data: ReservationUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(
        reservation_id, session
    )

    await check_reservation_intersections(
        **update_data.model_dump(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        reservation, update_data, session
    )
    return reservation
