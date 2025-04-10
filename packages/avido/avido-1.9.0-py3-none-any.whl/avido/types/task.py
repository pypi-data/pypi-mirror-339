# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .topic import Topic
from .._models import BaseModel
from .application import Application

__all__ = ["Task", "Definition"]


class Definition(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    modified_at: str = FieldInfo(alias="modifiedAt")

    name: str

    type: Literal["NATURALNESS", "STYLE", "RECALL", "LLMQA", "BLACKLIST"]
    """Type of evaluation. Valid options: NATURALNESS, STYLE, RECALL, LLMQA."""

    application: Optional[Application] = None
    """Application configuration and metadata"""

    global_config: Optional[object] = FieldInfo(alias="globalConfig", default=None)

    style_guide_id: Optional[str] = FieldInfo(alias="styleGuideId", default=None)


class Task(BaseModel):
    id: str
    """The unique identifier of the task"""

    application: Application
    """Application configuration and metadata"""

    created_at: str = FieldInfo(alias="createdAt")
    """The date and time the task was created"""

    definitions: List[Definition]

    description: str
    """The task description"""

    modified_at: str = FieldInfo(alias="modifiedAt")
    """The date and time the task was last updated"""

    title: str
    """The title of the task"""

    topic: Topic
    """Details about a single Topic"""

    input_examples: Optional[object] = FieldInfo(alias="inputExamples", default=None)
    """Example inputs for the task"""

    last_test: Optional[str] = FieldInfo(alias="lastTest", default=None)
    """The date and time this task was last tested"""

    pass_rate: Optional[float] = FieldInfo(alias="passRate", default=None)
    """The 30 day pass rate for the task measured in percentage"""
