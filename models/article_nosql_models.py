from pydantic import BaseModel, Field, field_validator
from typing import List, Set
from . import DOI_REGEX


class Author(BaseModel):
    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)


class Image(BaseModel):
    image_number: str = Field(..., min_length=1)
    file_path: str = Field(..., min_length=1)


class Table(BaseModel):
    table_number: str = Field(..., min_length=1)
    file_path: str = Field(..., min_length=1)


class ArticleTextDBSchema(BaseModel):
    id: str = Field(..., pattern=DOI_REGEX, description='Valid DOI format')
    title: str = Field(..., min_length=1, description='Title of the article')
    authors: List[Author] = Field(..., min_length=1, description='At least one author required')
    abstract: str = Field(..., min_length=1, description='Abstract of the article')
    keywords: Set[str]
    markdown_full_text: str = Field(..., min_length=1, description='Full article text in Markdown format')
    images: List[Image] = []
    tables: List[Table] = []

    @field_validator('keywords', mode='before')
    @classmethod
    def validate_keywords(cls, value):
        """Ensure keywords are a set, not a list."""
        if not isinstance(value, set):
            raise ValueError('Keywords must be a set, not a list')
        return value
