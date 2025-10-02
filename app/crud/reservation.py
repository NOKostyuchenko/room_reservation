from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.reservation import Reservation


class CRUDReservation(CRUDBase):
    

    @staticmethod
    async def get_reservations_at_the_same_time(
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        session: AsyncSession
    ) -> list[Reservation]:
        
        db_object = await session.execute(
            select(Reservation).where(
                and_(
                    Reservation.meetingroom_id == meetingroom_id,
                    Reservation.from_reserve <= to_reserve,
                    Reservation.to_reserve >= from_reserve
                )
            )  
        )

        return db_object.all()


reservation_crud = CRUDReservation(Reservation)