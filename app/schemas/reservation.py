from datetime import datetime

from pydantic import BaseModel, field_validator, model_validator


class ReservationBase(BaseModel):
    from_reverse: datetime
    to_reverse: datetime


class ReservationUpdate(ReservationBase):
    

    @field_validator("from_reverse")
    def check_from_reserve_later_than_now(cls, from_reverse: datetime):
        if datetime.now() >= from_reverse:
            raise ValueError("You can't book retroactively!")
        return from_reverse
    

    @model_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, reservation: dict):
        if reservation["from_reverse"] >= reservation["to_reverse"]:
            raise ValueError("The end time of the booking cannot be less than the start time!")
        return reservation


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDelete(ReservationBase):
    id: int
    meetingroom_id: int

