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

