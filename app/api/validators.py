from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.meeting_room import MeetingRoom
from crud.meeting_room import meeting_room_crud


async def check_name_dublicate(
    room_name: str,
    session: AsyncSession
) -> None:
    
    room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)

    if room_id is not None:
        raise HTTPException(status_code=422,
                            detail="There is already a meeting room with what name!")


async def check_meeting_room_exists(
    meeting_room_id: int,
    session: AsyncSession
) -> MeetingRoom:
    
    meeting_room = await meeting_room_crud.get(meeting_room_id, session)

    if meeting_room is None:
        raise HTTPException(status_code=404,
                            detail="Meeting room not found!")
    return meeting_room