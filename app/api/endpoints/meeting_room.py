from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from crud.meeting_room import meeting_room_crud
from schemas.meeting_room import (MeetingRoomCreate, MeetingRoomDB,
                                  MeetingRoomUpdate)
from api.validators import check_meeting_room_exists, check_name_dublicate
from schemas.reservation import ReservationDB
from crud.reservation import reservation_crud

router = APIRouter()


@router.post(
    "/",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session: AsyncSession = Depends(get_async_session)
):

    await check_name_dublicate(meeting_room.name, session)

    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room


@router.get(
    "/",
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session)
):
    
    list_rooms = await meeting_room_crud.get_multi(session)
    return list_rooms


@router.patch(
    "/{meeting_room_id}",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True
)
async def partially_update_meeting_room(
    meeting_room_id: int,
    update_data: MeetingRoomUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)

    if update_data.name is not None:
        await check_name_dublicate(update_data.name, session)

    meeting_room = await meeting_room_crud.update(meeting_room, update_data, session)
    return meeting_room


@router.delete(
    "/{meeting_room_id}",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True
)
async def remove_meeting_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    
    meeting_room = await check_meeting_room_exists(meeting_room_id, session)
    db_room = await meeting_room_crud.delete(meeting_room, session)

    return db_room



@router.get(
    "/{meeting_room_id}/reservations",
    response_model=list[ReservationDB]
)
async def get_reservations_for_room(
    meeting_room_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    await check_meeting_room_exists(meeting_room_id, session)
    reservations: list = await reservation_crud.get_future_reservations_for_room(
        meeting_room_id, session
    )
    return reservations