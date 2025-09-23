from fastapi import APIRouter, HTTPException

from crud.meeting_room import create_meeting_room, get_romm_id_by_name
from schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB

router = APIRouter()

@router.post("/meeting_rooms/", response_model=MeetingRoomDB, response_model_exclude_none=True)
async def create_new_meeting_room(
    meeting_room: MeetingRoomCreate
):
    room_id = await get_romm_id_by_name(meeting_room.name)

    if room_id is not None:
        raise HTTPException(status_code=422, detail="There is already a meeting room with what name")

    new_room = await create_meeting_room(meeting_room)
    return new_room