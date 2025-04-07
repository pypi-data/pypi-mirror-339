from drf_pydantic import BaseModel as DRFBaseModel
from pydantic import Field, BaseModel
from typing import List, Optional

from .form import MessageHistory, UserInfo
from .analytics import AnalyticsResult


class Pyndatic2FormMetadata(BaseModel):
    """Base class for defining the structure of a specific form."""
    next_message_ai: str = ""
    next_message_language: str = "en"
    progress: int = 0
    user_info: Optional[UserInfo] = None
    user_language: str = "en"


class Pyndatic2SessionInfo(DRFBaseModel):
    """Base class for defining the structure of a specific form."""
    metadata: Pyndatic2FormMetadata = Field(default_factory=Pyndatic2FormMetadata)
    user_form: str = Field(default="{}", description="JSON string representation of form data")


class Pyndatic2System(BaseModel):
    """Base class for defining the structure of a specific form."""
    completion_threshold: int = Field(default=100)
    completion_achieved: bool = Field(default=False)
    session_id: Optional[str] = None
    client_id: Optional[str] = None
    role_prompt: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = None
    form_defaults: str = Field(default="{}", description="JSON string representation of form defaults")


class Pyndatic2AgentResponse(DRFBaseModel):
    """Base class for defining the structure of a specific form."""
    session_info: Pyndatic2SessionInfo = Field(default_factory=Pyndatic2SessionInfo)
    system: Pyndatic2System = Field(default_factory=Pyndatic2System)
    analytics: Optional[AnalyticsResult] = None
    history: Optional[List[MessageHistory]] = Field(default_factory=list)
