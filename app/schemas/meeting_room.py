from typing import Optional

from pydantic import BaseModel, Field, field_validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None)


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=2, max_length=100)


class MeetingRoomDB(MeetingRoomCreate):
    id: int


class MeetingRoomUpdate(MeetingRoomBase):
    
    @field_validator("name")
    def checking_the_name_for_compliance(cls, name: str):
        if name is None:
            raise ValueError("The name of the meeting room cannot be empty!")
        return name
    
