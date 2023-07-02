from typing import Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class PluginRequest(GenericModel, Generic[DataT]):
    """Base model for all plugin requests."""
    relationship_token: str
    data: DataT


class PluginResponse(GenericModel, Generic[DataT]):
    """Base model for all plugin responses."""
    success: bool
    data: Optional[DataT] = None
    error: Optional[str] = None
    forced_response: Optional[str] = None


class EmptyData(BaseModel):
    """Model that represents that no data is received."""
    pass

# Custom models:
class PluginRequest(BaseModel):
    pass


class PluginResponse(BaseModel):
    success: bool
    data: dict


class EmptyData(BaseModel):
    pass