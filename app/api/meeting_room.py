from fastapi import APIRouter, HTTPException, Depends

from core.db import get_async_session
from crud.meeting_room import create_meeting_room, get_room_id_by_name, read_all_rooms_from_db
from schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB

router = APIRouter()

@router.post(
    "/meeting_rooms/",
    response_model=MeetingRoomDB,
    response_model_exclude_none=True
)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate,
    session = Depends(get_async_session)
):
    room_id = await get_room_id_by_name(meeting_room.name, session)

    if room_id is not None:
        raise HTTPException(status_code=422, detail="There is already a meeting room with what name!")

    new_room = await create_meeting_room(meeting_room, session)
    return new_room

@router.get(
    "/meeting_rooms/",
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True
)
async def get_all_meeting_rooms(
    session = Depends(get_async_session)
):
    list_rooms = await read_all_rooms_from_db(session)
    return list_rooms
