from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from datetime import datetime
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.reservation import Reservation


class CRUDReservation(CRUDBase):
    

    @staticmethod
    async def get_reservations_at_the_same_time(
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: Optional[int] = None,
        session: AsyncSession
    ) -> list[Reservation]:
        
        select_stmt = select(Reservation).where(
            and_(
                Reservation.meetingroom_id == meetingroom_id,
                Reservation.from_reserve <= to_reserve,
                Reservation.to_reserve >= from_reserve
            )
        )

        if reservation_id is not None:
            select_stmt = select_stmt.where(
                Reservation.id != reservation_id
            )
        
        reservations = await session.execute(select_stmt)
        return reservations.all()


    @staticmethod
    async def get_future_reservations_for_room(
        meetingroom_id: int,
        session: AsyncSession
    ) -> list[Reservation]:
        select_stmt = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            Reservation.to_reserve > datetime.now()
        )
        reservations = await session.execute(select_stmt)
        return reservations.scalars().all()


reservation_crud = CRUDReservation(Reservation)