import pytest
from pydantic import ValidationError
from models.article_sql_models import ArticleMetadataDBSchema, ArticlePDFDBSchema

test_cases = [
    {
        'article_metadata': {
            'id': '10.1000/123456',
            'title': 'Test Article',
            'authors': 'John Doe, Jane Smith',
            'journal': 'Test Journal',
            'year': 2024,
            'volume': 1,
            'pages': '10-20',
            'keywords': 'science, research'
        },
        'is_valid': True,
        'expected_exception': None
    },
    {
        'article_metadata': {
            'id': '11.1000/123456',
            'title': 'Test Article',
            'authors': 'John Doe, Jane Smith',
            'journal': 'Test Journal',
            'year': 2024,
            'volume': 1,
            'pages': '10-20',
            'keywords': 'science, research'
        },
        'is_valid': False,
        'expected_exception': ValidationError
    },
    {
        'article_metadata': {
            'title': 'Test Article',
            'authors': 'John Doe, Jane Smith',
            'journal': 'Test Journal',
            'year': 2024,
            'volume': 1,
            'pages': '10-20',
            'keywords': 'science, research'
        },
        'is_valid': False,
        'expected_exception': ValidationError
    },
    {
        'article_metadata': {
            'id': '10.1000/123456',
            'title': 'Test Article',
            'authors': 'John Doe, Jane Smith',
            'journal': 'Test Journal',
            'year': 2024,
            'volume': -1,
            'pages': '10-20',
            'keywords': 'science, research'
        },
        'is_valid': False,
        'expected_exception': ValidationError
    }
]


@pytest.mark.parametrize("test_data", test_cases)
def test_article_metadata(test_data):
    if test_data['is_valid']:
        article = ArticleMetadataDBSchema(**test_data['article_metadata'])

        for key, value in test_data['article_metadata'].items():
            assert getattr(article, key) == value
    else:
        with pytest.raises(test_data['expected_exception']):
            ArticleMetadataDBSchema(**test_data['article_metadata'])


pdf_test_cases = [
    {
        'article_pdf': {
            'id': '10.1000/123456',
            'file_path': '/valid/path/to/file.pdf',
        },
        'is_valid': True,
        'expected_values': {'is_pdf_available': True}
    },
    {
        'article_pdf': {
            'id': '10.1000/123456',
            'file_path': None,
        },
        'is_valid': True,
        'expected_values': {'is_pdf_available': False}
    },
    {
        'article_pdf': {
            'id': 'invalid_doi',
            'file_path': '/valid/path/to/file.pdf',
        },
        'is_valid': False,
        'expected_exception': ValidationError
    },
    {
        'article_pdf': {
            'id': '10.1000/123456',
            'file_path': 'path/to/file>',
        },
        'is_valid': False,
        'expected_exception': ValidationError
    }
]


@pytest.mark.parametrize("test_data", pdf_test_cases)
def test_article_pdf(test_data):
    if test_data['is_valid']:
        pdf = ArticlePDFDBSchema(**test_data['article_pdf'])

        for key, value in test_data['article_pdf'].items():
            assert getattr(pdf, key) == value

        for key, value in test_data['expected_values'].items():
            assert getattr(pdf, key) == value
    else:
        with pytest.raises(test_data['expected_exception']):
            ArticlePDFDBSchema(**test_data['article_pdf'])
