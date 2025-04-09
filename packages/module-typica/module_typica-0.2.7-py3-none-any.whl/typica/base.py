import uuid

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class StringIdentifier(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Identifier of data with string uuidv4",
        examples=["f82192c2460965cd0a9ce68305c1969a4"],
    )


class StringIdentifier_(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        alias="_id",
        description="Identifier of data with string uuidv4",
        examples=["f82192c2460965cd0a9ce68305c1969a4"],
    )


class UUIDIdentifier(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Identifier of data with UUID format",
        examples=["f82192c2460965cd0a9ce68305c1969a4"],
    )

    @model_validator(mode="before")
    def validate_uuid(cls, values):
        """
        Validate if id is str, then convert to uuid.UUID
        """

        if isinstance(values.get("id"), str):
            values["id"] = uuid.UUID(values["id"])
        return values


class UUIDIdentifier_(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        alias="_id",
        description="Identifier of data with UUID format",
        examples=["f82192c2460965cd0a9ce68305c1969a4"],
    )

    @model_validator(mode="before")
    def validate_uuid(cls, values):
        """
        Validate if _id is str, then convert to uuid.UUID
        """
        if isinstance(values.get("_id"), str):
            values["_id"] = uuid.UUID(values["_id"])
        return values


class CreationMeta(BaseModel):
    created_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        description="When data was created",
        examples=["2022-08-08T00:00:00.000000+00:00", 1661416000, 1661416000000],
    )
    created_by: Optional[str] = Field(None, description="Whos created the data")

    @model_validator(mode="before")
    def validate_created_at(cls, values):
        """
        Validate if created_at is str, then convert to datetime
        If created_at is int, then convert to datetime using fromtimestamp
        If created_at is int and length is more than 10, then divide by 1000 first
        """
        if isinstance(values.get("created_at"), str):
            values["created_at"] = datetime.fromisoformat(values["created_at"])
        if isinstance(values.get("created_at"), int):
            if str(values["created_at"]).__len__() <= 10:
                values["created_at"] = datetime.fromtimestamp(values["created_at"])
            else:
                values["created_at"] = datetime.fromtimestamp(
                    int(values["created_at"] / 1000)
                )
        return values
