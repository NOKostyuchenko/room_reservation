from typing import Optional

from sqlalchemy import select

from core.db import AsyncSessionLocal
from schemas.meeting_room import MeetingRoomCreate
from models.meeting_room import MeetingRoom


async def create_meeting_room(new_room: MeetingRoomCreate) -> MeetingRoom:
    
    new_room_data: dict = new_room.model_dump()
    db_room: MeetingRoom = MeetingRoom(**new_room_data)
    
    async with AsyncSessionLocal() as session:
        session.add(db_room)
        await session.commit()
        await session.refresh(db_room)

    return db_room


async def get_romm_id_by_name(room_name: str) -> Optional[int]:
    async with AsyncSessionLocal() as session:

        db_room_id = await session.execute(select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        ))

        db_room_id = db_room_id.scalars().first()
    
    return db_room_id


