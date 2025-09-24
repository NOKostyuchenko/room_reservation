from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.meeting_room import MeetingRoomCreate
from models.meeting_room import MeetingRoom


async def create_meeting_room(
    new_room: MeetingRoomCreate,
    session: AsyncSession
) -> MeetingRoom:
    
    new_room_data: dict = new_room.model_dump()
    db_room: MeetingRoom = MeetingRoom(**new_room_data)
    
    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)

    return db_room


async def get_room_id_by_name(
    room_name: str,
    session: AsyncSession
) -> Optional[int]:
    
    db_room_id = await session.execute(select(MeetingRoom.id).where(
        MeetingRoom.name == room_name
    ))

    db_room_id = db_room_id.scalars().first()
    
    return db_room_id


async def read_all_rooms_from_db(
    session: AsyncSession
) -> list[MeetingRoom]:
    db_rooms = await session.scalars(select(MeetingRoom))
    list_records = db_rooms.all()
    return list_records
