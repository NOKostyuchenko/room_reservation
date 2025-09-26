from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from crud.meeting_room import (create_meeting_room, get_room_id_by_name,
                               read_all_rooms_from_db, update_meeting_room,
                               get_meeting_room_by_id)
from schemas.meeting_room import (MeetingRoomCreate, MeetingRoomDB,
                                  MeetingRoomUpdate)

router = APIRouter(prefix="/meeting_rooms", tags=["Meeting Rooms"])


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

    new_room = await create_meeting_room(meeting_room, session)
    return new_room


@router.get(
    "/",
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
    session: AsyncSession = Depends(get_async_session)
):
    
    list_rooms = await read_all_rooms_from_db(session)
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
    meeting_room = await get_meeting_room_by_id(meeting_room_id, session)

    if meeting_room is None:
        raise HTTPException(status_code=404,
                            detail="Meeting room not found!")

    if update_data.name is not None:
        await check_name_dublicate(update_data.name, session)

    meeting_room = await update_meeting_room(meeting_room, update_data, session)
    return meeting_room

async def check_name_dublicate(
    room_name: str,
    session: AsyncSession
) -> None:
    
    room_id = await get_room_id_by_name(room_name, session)

    if room_id is not None:
        raise HTTPException(status_code=422,
                            detail="There is already a meeting room with what name!")
