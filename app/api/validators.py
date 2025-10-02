from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.meeting_room import MeetingRoom
from crud.meeting_room import meeting_room_crud
from crud.reservation import reservation_crud
from models.reservation import Reservation


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


async def check_reservation_intersections(**kwargs) -> None:
    reservations: list = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs
    )
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations)
        )


async def check_reservation_before_edit(
    reservation_id: int,
    session: AsyncSession
) -> Reservation:
    reservation = await reservation_crud.get(reservation_id, session)
    if reservation is None:
        raise HTTPException(status_code=404,
                            detail="Reservation not found!")
    return reservation