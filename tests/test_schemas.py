import pytest
import os
from io import BytesIO
from pydantic import ValidationError

from models.article_nosql_models import Author
from models.schemas import ArticlePDFFile, ResponseSchema, StatusEnum, ArticleMetadata


def load_pdf(file_path):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, file_path)

    if os.path.isfile(full_path):
        with open(full_path, 'rb') as f:
            return BytesIO(f.read())
    return None


test_cases_article_pdf = [
    {
        'article_pdf': {
            'id': '10.1000/10/123456',
            'is_available': True,
            'pdf_file': 'tests/pdf/example.pdf',
        },
        'expected_exception': None,
        'is_valid': True,
        'test_description': 'Valid ArticlePDFFile with pdf_file',
    },
    {
        'article_pdf': {
            'id': '10.1000/10/123456',
            'is_available': False,
            'pdf_file': None,
        },
        'expected_exception': None,
        'is_valid': True,
        'test_description': 'Valid ArticlePDFFile without pdf_file',
    },
    {
        'article_pdf': {
            'id': 'invalid_doi',
            'is_available': True,
            'pdf_file': 'pdf/example.pdf',
        },
        'expected_exception': ValueError,
        'is_valid': False,
        'test_description': 'Invalid DOI format in ArticlePDFFile',
    },
    {
        'article_pdf': {
            'id': '10.1000/10/123456',
            'is_available': 'not_a_bool',
            'pdf_file': 'pdf/example.pdf',
        },
        'expected_exception': ValueError,
        'is_valid': False,
        'test_description': 'Invalid is_available type in ArticlePDFFile',
    },
]


@pytest.mark.parametrize('test_data', test_cases_article_pdf,
                         ids=[case['test_description'] for case in test_cases_article_pdf])
def test_article_pdf(test_data):
    if test_data['is_valid']:

        if isinstance(test_data['article_pdf']['pdf_file'], str):
            pdf_file = load_pdf(test_data['article_pdf']['pdf_file'])
            test_data['article_pdf']['pdf_file'] = pdf_file

        article_pdf = ArticlePDFFile(**test_data['article_pdf'])
        assert article_pdf.is_available == test_data['article_pdf']['is_available']
        for key, value in test_data['article_pdf'].items():
            assert getattr(article_pdf, key) == value
    else:
        with pytest.raises(test_data['expected_exception']):
            ArticlePDFFile(**test_data['article_pdf'])


test_cases_response_schema = [
    {
        'test_description': 'Valid ResponseSchema with SUCCESS status',
        'response_data': {
            'status': StatusEnum.SUCCESS,
            'message': 'Request processed successfully.',
            'error_code': None,
            'data': {'id': '10.1000/10/123456'},
            'http_status': 200
        },
        'is_valid': True,
        'expected_exception': None
    },
    {
        'test_description': 'Valid ResponseSchema with ERROR status',
        'response_data': {
            'status': StatusEnum.ERROR,
            'message': 'An error occurred.',
            'error_code': 'AML-1',
            'data': None,
            'http_status': 200
        },
        'is_valid': True,
        'expected_exception': None
    },
    {
        'test_description': 'Invalid status in ResponseSchema',
        'response_data': {
            'status': 'INVALID_STATUS',
            'message': 'Invalid status test.',
            'error_code': None,
            'data': None,
            'http_status': 400
        },
        'is_valid': False,
        'expected_exception': ValidationError
    },
    {
        'test_description': 'Missing status in ResponseSchema',
        'response_data': {
            'message': 'Missing status.',
            'error_code': None,
            'data': None,
            'http_status': 400
        },
        'is_valid': False,
        'expected_exception': ValidationError
    }
]


@pytest.mark.parametrize('test_data', test_cases_response_schema,
                         ids=[case['test_description'] for case in test_cases_response_schema])
def test_response_schema(test_data):
    if test_data['is_valid']:
        response_schema = ResponseSchema(**test_data['response_data'])
        for key, value in test_data['response_data'].items():
            assert getattr(response_schema, key) == value
    else:
        with pytest.raises(test_data['expected_exception']):
            ResponseSchema(**test_data['response_data'])


test_cases_article_metadata = [
    {
        'article_metadata': {
            'id': '10.1000/10/123456',
            'title': 'Example Article Title',
            'authors': [{'name': 'John', 'surname': 'Smith'}],
            'keywords': {'keyword1', 'keyword2'},
            'journal': 'Example Journal',
            'year': 2022,
            'volume': 10,
            'issue': 2,
            'pages': '23-34'
        },
        'expected_exception': None,
        'is_valid': True,
        'test_description': 'Valid ArticleMetadataRequest',
    },
    {
        'article_metadata': {
            'id': '',
            'title': 'Example Article Title',
            'authors': [{'name': 'John', 'surname': 'Smith'}],
            'keywords': {'keyword1', 'keyword2'},
            'journal': 'Example Journal',
            'year': 2022,
            'volume': 10,
            'issue': 2,
            'pages': '23-34'
        },
        'expected_exception': ValueError,
        'is_valid': False,
        'test_description': 'Invalid DOI format',
    },
    {
        'article_metadata': {
            'id': '10.1000/10/123456',
            'title': '',
            'authors': [{'name': 'John', 'surname': 'Smith'}],
            'keywords': {'keyword1', 'keyword2'},
            'journal': 'Example Journal',
            'year': 2022,
            'volume': 10,
            'issue': 2,
            'pages': '23-34'
        },
        'expected_exception': ValueError,
        'is_valid': False,
        'test_description': 'Missing title in ArticleMetadataRequest',
    },
    {
        'article_metadata': {
            'id': '10.1000/10/123456',
            'title': 'Example Article Title',
            'authors': [{'name': 'John', 'surname': 'Smith'}],
            'keywords': {'keyword1', 'keyword2'},
            'journal': 'Example Journal',
            'year': 2022,
            'volume': 10,
            'issue': 2,
            'pages': ''
        },
        'expected_exception': ValueError,
        'is_valid': False,
        'test_description': 'Missing page range in ArticleMetadataRequest',
    },
    {
        'article_metadata': {
            'id': '10.1000/10/123456',
            'title': 'Example Article Title',
            'authors': [],
            'keywords': {'keyword1', 'keyword2'},
            'journal': 'Example Journal',
            'year': 2022,
            'volume': 10,
            'issue': 2,
            'pages': '23-34',
        },
        'expected_exception': ValueError,
        'is_valid': False,
        'test_description': 'Missing authors in ArticleMetadataRequest',
    },
]


@pytest.mark.parametrize('test_data', test_cases_article_metadata,
                         ids=[case['test_description'] for case in test_cases_article_metadata])
def test_article_metadata(test_data):
    if test_data['is_valid']:
        article_metadata = ArticleMetadata(**test_data['article_metadata'])
        for key, value in test_data['article_metadata'].items():
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                expected_value = [Author(**v) for v in value]
            elif isinstance(value, set):
                expected_value = set(value)
            else:
                expected_value = value
            assert getattr(article_metadata, key) == expected_value
    else:
        with pytest.raises(test_data['expected_exception']):
            ArticleMetadata(**test_data['article_metadata'])
