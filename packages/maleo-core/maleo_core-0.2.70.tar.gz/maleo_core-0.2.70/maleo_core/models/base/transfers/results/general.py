from __future__ import annotations
from datetime import datetime, date
from pydantic import BaseModel, Field, field_serializer
from pydantic_core.core_schema import FieldSerializationInfo
from typing import Literal, Optional, Union, Any
from uuid import UUID
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters

class BaseGeneralResults:
    class UniqueIdentifiers(BaseModel):
        id:int = Field(..., ge=1, description="Data's ID, must be >= 1.")
        uuid:UUID = Field(..., description="Data's UUID.")

        @field_serializer('uuid')
        def serialize_uuid(self, value:UUID, info:FieldSerializationInfo) -> str:
            """Serializes UUID to a hex string."""
            return str(value)

    class Timestamp(BaseModel):
        created_at:datetime = Field(..., description="Data's created_at timestamp")
        updated_at:datetime = Field(..., description="Data's updated_at timestamp")

        @field_serializer('created_at', 'updated_at')
        def serialize_timestamps(self, value:Union[datetime, date], info:FieldSerializationInfo) -> str:
            """Serializes datetime/date fields to ISO format."""
            return value.isoformat()

    class Status(BaseModel):
        is_deleted:bool = Field(..., description="Data's deletion status.")
        is_active:bool = Field(..., description="Data's active status.")
        status:BaseGeneralModels.StatusType = Field(..., description="Data's status")

    #* ----- ----- ----- Base ----- ----- ----- *#
    class Base(BaseModel):
        success:bool = Field(..., description="Success status")
        message:Optional[str] = Field(None, description="Optional message")
        description:Optional[str] = Field(None, description="Optional description")

    #* ----- ----- ----- Derived ----- ----- ----- *#
    class Fail(Base):
        success:Literal[False] = Field(False, description="Success status")
        other:Optional[Any] = Field(None, description="Optional other information")

    class SingleData(Base):
        success:Literal[True] = Field(True, description="Success status")
        data:Any = Field(..., description="Fetched data")
        other:Optional[Any] = Field(None, description="Optional other information")

    class MultipleData(
        Base,
        BaseGeneralModels.SimplePagination
    ):
        total_data:int = Field(..., description="Total data count")
        success:Literal[True] = Field(True, description="Success status")
        data:list[Any] = Field(..., description="Paginated data")
        pagination:BaseGeneralModels.ExtendedPagination = Field(..., description="Pagination metadata")
        other:Optional[Any] = Field(None, description="Optional other information")

    class BaseStatusUpdateResponse(BaseModel):
        message:str = Field(..., description="Status update response message")
        update_description:str = Field(..., description="Status update on update response description")
        maintain_description:str = Field(..., description="Status update on maintain response description")

    BaseStatusUpdateResponseMappings = dict[BaseGeneralParameters.StatusUpdateAction, BaseStatusUpdateResponse]

    class StatusUpdateResponseContent(BaseModel):
        message:str = Field(..., description="Status update response message")
        description:str = Field(..., description="Status update response description")

    class StatusUpdateValidation(BaseModel):
        is_status_update_needed:bool = Field(..., description="Flag whether or not status update is needed")
        response_content:BaseGeneralResults.StatusUpdateResponseContent = Field(..., description="Status update response content")

    @staticmethod
    def needs_status_update(action:BaseGeneralParameters.StatusUpdateAction, status:BaseGeneralModels.StatusType) -> bool:
        status_mapping = {
            BaseGeneralParameters.StatusUpdateAction.DELETE: lambda s: s != BaseGeneralModels.StatusType.DELETED,
            BaseGeneralParameters.StatusUpdateAction.RESTORE: lambda s: s == BaseGeneralModels.StatusType.DELETED,
            BaseGeneralParameters.StatusUpdateAction.DEACTIVATE: lambda s: s != BaseGeneralModels.StatusType.INACTIVE,
            BaseGeneralParameters.StatusUpdateAction.ACTIVATE: lambda s: s != BaseGeneralModels.StatusType.ACTIVE,
        }
        return status_mapping.get(action, lambda _: False)(status)

    @staticmethod
    def validate_status_update(
        name:str,
        action:BaseGeneralParameters.StatusUpdateAction,
        status:BaseGeneralModels.StatusType
    ) -> StatusUpdateValidation:
        status_update_responses = {
            BaseGeneralParameters.StatusUpdateAction.DELETE: ("deleted", "deleted", "is_deleted", "true"),
            BaseGeneralParameters.StatusUpdateAction.RESTORE: ("restored", "not deleted", "is_deleted", "false"),
            BaseGeneralParameters.StatusUpdateAction.DEACTIVATE: ("deactivated", "inactive", "is_active", "false"),
            BaseGeneralParameters.StatusUpdateAction.ACTIVATE: ("activated", "active", "is_active", "true"),
        }
        
        action_data = status_update_responses.get(action)
        if not action_data:
            raise ValueError(f"Invalid status update action: {action}")

        update_text, maintain_text, field_name, new_value = action_data
        is_update_needed = BaseGeneralResults.needs_status_update(action, status)

        return BaseGeneralResults.StatusUpdateValidation(
            is_status_update_needed=is_update_needed,
            response_content=BaseGeneralResults.StatusUpdateResponseContent(
                message=f"{name} successfully {update_text}",
                description=f"{name}'s `{field_name}` status changed to `{new_value}`" if is_update_needed else f"{name} is currently {maintain_text}, no data changed"
            )
        )