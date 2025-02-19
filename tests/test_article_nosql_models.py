import pytest
from article_models.article_nosql_models import ArticleText, Author, Image, Table

test_cases = [
    {
        'test_description': 'ArticleText is valid',
        'article': {
            'id': '10.1000/10/123456',
            'title': 'Example Title',
            'authors': [{'name': 'John', 'surname': 'Doe'}, {'name': 'Maria', 'surname': 'Nowak'}],
            'abstract': 'This is an abstract.',
            'keywords': {'science', 'research', 'AI'},
            'markdown_full_text': '## Introduction\nThis is a sample markdown text.',
            'images': [{'image_number': 'fig.1.3', 'file_path': '/images/fig1.3.png'}],
            'tables': [{'table_number': 'tab.2.1', 'file_path': '/tables/table2.1.csv'}]
        },
        'is_valid': True,
        'expected_exception': None
    },
    {
        'test_description': 'Invalid DOI format',
        'article': {
            'id': 'invalid_doi',
            'title': 'Example Title',
            'authors': [{'name': 'John', 'surname': 'Doe'}],
            'abstract': 'Abstract text',
            'keywords': {'science'},
            'markdown_full_text': 'Markdown text'
        },
        'is_valid': False,
        'expected_exception': ValueError
    },
    {
        'test_description': 'No authors in ArticleText',
        'article': {
            'id': '10.1000/10/123456',
            'title': 'Example Title',
            'authors': [],
            'abstract': 'Abstract text',
            'keywords': {'science'},
            'markdown_full_text': 'Markdown text'
        },
        'is_valid': False,
        'expected_exception': ValueError
    },
    {
        'test_description': 'Empty title',
        'article': {
            'id': '10.1000/10/123456',
            'title': '',
            'authors': [{'name': 'John', 'surname': 'Doe'}],
            'abstract': 'Abstract text',
            'keywords': {'science'},
            'markdown_full_text': 'Markdown text'
        },
        'is_valid': False,
        'expected_exception': ValueError
    },
    {
        'test_description': 'Keywords as a list instead of a set',
        'article': {
            'id': '10.1000/10/123456',
            'title': 'Example Title',
            'authors': [{'name': 'John', 'surname': 'Doe'}],
            'abstract': 'Abstract text',
            'keywords': ['science', 'AI'],
            'markdown_full_text': 'Markdown text'
        },
        'is_valid': False,
        'expected_exception': ValueError
    },
    {
        'test_description': 'Missing table_number or file_path in tables',
        'article': {
            'id': '10.1000/10/123456',
            'title': 'Example Title',
            'authors': [{'name': 'John', 'surname': 'Doe'}],
            'abstract': 'Abstract text',
            'keywords': {'science'},
            'markdown_full_text': 'Markdown text',
            'tables': [{'table_number': '', 'file_path': ''}]
        },
        'is_valid': False,
        'expected_exception': ValueError
    },
    {
        'test_description': 'Missing image_number or file_path in images',
        'article': {
            'id': '10.1000/10/123456',
            'title': 'Example Title',
            'authors': [{'name': 'John', 'surname': 'Doe'}],
            'abstract': 'Abstract text',
            'keywords': {'science'},
            'markdown_full_text': 'Markdown text',
            'images': [{'image_number': '', 'file_path': ''}]
        },
        'is_valid': False,
        'expected_exception': ValueError
    },
    {
        'test_description': 'Authors missing surname',
        'article': {
            'id': '10.1000/10/123456',
            'title': 'Example Title',
            'authors': [{'name': 'John'}],
            'abstract': 'Abstract text',
            'keywords': {'science'},
            'markdown_full_text': 'Markdown text'
        },
        'is_valid': False,
        'expected_exception': ValueError
    },
    {
        'test_description': 'Multiple errors (no authors, empty title, invalid DOI)',
        'article': {
            'id': 'invalid_doi',
            'title': '',
            'authors': [],
            'abstract': 'Abstract text',
            'keywords': {'science'},
            'markdown_full_text': 'Markdown text'
        },
        'is_valid': False,
        'expected_exception': ValueError
    }
]


@pytest.mark.parametrize(
    'test_data',
    test_cases,
    ids=[case['test_description'] for case in test_cases]
)
def test_article_text(test_data):
    if test_data['is_valid']:
        article = ArticleText(**test_data['article'])

        for key, value in test_data['article'].items():
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                expected_value = [Author(**v) if key == 'authors' else Image(**v) if key == 'images' else Table(**v) for
                                  v in value]
            elif isinstance(value, set):
                expected_value = set(value)
            else:
                expected_value = value
            assert getattr(article, key) == expected_value
    else:
        with pytest.raises(test_data['expected_exception']):
            ArticleText(**test_data['article'])
