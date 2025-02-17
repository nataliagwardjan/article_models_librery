from pydantic import BaseModel, Field, model_validator
from typing import Optional
from . import DOI_REGEX, PAGES_REGEX

PATH_REGEX = r'^[\w\-. /\\:]+$'


class ArticleMetadataDBSchema(BaseModel):
    id: str = Field(..., pattern=DOI_REGEX, description='Valid DOI format')
    title: str = Field(..., min_length=1)
    authors: str = Field(..., min_length=1, description='Comma-separated list of authors')
    journal: str = Field(..., min_length=1)
    year: int = Field(..., ge=0)
    volume: int = Field(..., ge=0)
    issue: Optional[int] = None
    pages: str = Field(..., pattern=PAGES_REGEX, description='Page range format: 23-34')
    keywords: str = Field(..., min_length=1, description='Comma-separated list of keywords')


class ArticlePDFDBSchema(BaseModel):
    id: str = Field(..., pattern=DOI_REGEX, description='Valid DOI format')
    file_path: Optional[str] = Field(None, pattern=PATH_REGEX, description='Path format')
    is_pdf_available: bool = Field(default=False)

    @model_validator(mode='before')
    @classmethod
    def set_is_pdf_available(cls, values):
        values['is_pdf_available'] = values.get('file_path') is not None
        return values
