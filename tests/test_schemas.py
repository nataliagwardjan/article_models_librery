import pytest
import os
from io import BytesIO
from pydantic import ValidationError
from models.schemas import ArticlePDFFile, ResponseSchema, StatusEnum


def load_pdf(file_path):
    if file_path and os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            return BytesIO(f.read())
    return None

# Test cases
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
            'pdf_file': 'tests/pdf/example.pdf',
        },
        'expected_exception': ValueError,
        'is_valid': False,
        'test_description': 'Invalid DOI format in ArticlePDFFile',
    },
    {
        'article_pdf': {
            'id': '10.1000/10/123456',
            'is_available': 'not_a_bool',
            'pdf_file': 'tests/pdf/example.pdf',
        },
        'expected_exception': ValueError,
        'is_valid': False,
        'test_description': 'Invalid is_available type in ArticlePDFFile',
    },
]


@pytest.mark.parametrize('test_data', test_cases_article_pdf, ids=[case['test_description'] for case in test_cases_article_pdf])
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
            'data': {'id': '10.1000/10/123456'}
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
            'data': None
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
            'data': None
        },
        'is_valid': False,
        'expected_exception': ValidationError
    },
    {
        'test_description': 'Missing status in ResponseSchema',
        'response_data': {
            'message': 'Missing status.',
            'error_code': None,
            'data': None
        },
        'is_valid': False,
        'expected_exception': ValidationError
    }
]

@pytest.mark.parametrize('test_data', test_cases_response_schema, ids=[case['test_description'] for case in test_cases_response_schema])
def test_response_schema(test_data):
    if test_data['is_valid']:
        response_schema = ResponseSchema(**test_data['response_data'])
        for key, value in test_data['response_data'].items():
            assert getattr(response_schema, key) == value
    else:
        with pytest.raises(test_data['expected_exception']):
            ResponseSchema(**test_data['response_data'])
