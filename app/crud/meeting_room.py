from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.meeting_room import MeetingRoom
from crud.base import CRUDBase
from schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate


class CRUDMeetingRoom(CRUDBase[
    MeetingRoom,
    MeetingRoomCreate,
    MeetingRoomUpdate
]):


    @staticmethod
    async def get_room_id_by_name(
        room_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        
        db_room_id = await session.execute(select(MeetingRoom.id).where(
            MeetingRoom.name == room_name
        ))
        db_room_id = db_room_id.scalars().first()
        return db_room_id


meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
