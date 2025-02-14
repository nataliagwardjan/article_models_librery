from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, Any
from io import BytesIO
from enum import Enum
from . import DOI_REGEX


class ArticlePDFFile(BaseModel):
    id: str = Field(..., pattern=DOI_REGEX, description="Valid DOI format")
    pdf_file: Optional[BytesIO] = None
    is_available: bool

    @model_validator(mode='before')
    @classmethod
    def set_is_pdf_available(cls, values):
        values['is_available'] = values.get('pdf_file') is not None
        return values

    model_config = ConfigDict(arbitrary_types_allowed=True)


class StatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class ResponseSchema(BaseModel):
    status: StatusEnum
    message: str
    error_code: Optional[str] = None
    data: Optional[Any] = None
