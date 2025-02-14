from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional, Any, List, Set
from io import BytesIO
from enum import Enum
from . import DOI_REGEX, PAGES_REGEX
from .article_nosql_models import Author


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

class ArticleMetadataRequest(BaseModel):
    id: str = Field(..., pattern=DOI_REGEX, description='Valid DOI format')
    title: str = Field(..., min_length=1, description='Title of the article')
    authors: List[Author] = Field(..., min_length=1, description='At least one author required')
    keywords: Set[str]
    journal: str = Field(..., min_length=1)
    year: int = Field(..., ge=0)
    volume: int = Field(..., ge=0)
    issue: Optional[int] = None
    pages: str = Field(..., pattern=PAGES_REGEX, description='Page range format: 23-34')

    @model_validator(mode='before')
    @classmethod
    def ensure_authors(cls, values):
        authors = values.get('authors', [])
        if isinstance(authors, list):
            values['authors'] = [Author(**author) if isinstance(author, dict) else author for author in authors]
        return values


class StatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class ResponseSchema(BaseModel):
    status: StatusEnum
    message: str
    error_code: Optional[str] = None
    data: Optional[Any] = None
