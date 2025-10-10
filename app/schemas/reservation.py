from datetime import datetime, timedelta

from pydantic import BaseModel, field_validator, model_validator, Field

FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(timespec="minutes")
TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec="minutes")


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(default=FROM_TIME)
    to_reserve: datetime = Field(default=TO_TIME)

    model_config = {"extra": "forbid"}


class ReservationUpdate(ReservationBase):
    

    @field_validator("from_reserve")
    def check_from_reserve_later_than_now(cls, from_reserve: datetime):
        if datetime.now() <= from_reserve:
            raise ValueError("You can't book retroactively!")
        return from_reserve
    

    @model_validator(mode="after")
    def check_from_reserve_before_to_reserve(
        cls,
        reservation: "ReservationCreate | ReservationUpdate"
    ) -> "ReservationCreate | ReservationUpdate":
        if reservation.from_reserve >= reservation.to_reserve:
            raise ValueError("The end time of the booking cannot be less than the start time!")
        return reservation


class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


class ReservationDelete(ReservationBase):
    id: int
    meetingroom_id: int


class ReservationDB(ReservationCreate):
    id: int

