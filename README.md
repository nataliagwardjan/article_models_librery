# Article Models Library

## Table of Contents

1. [Description](#description)
2. [Installation](#installation)
   - [Installing Locally](#installing-locally)
3. [Directory Structure](#directory-structure)
4. [Usage](#usage)
5. [Tests](#tests)

## Description

This library contains models for scientific articles, compatible with SQL, NoSQL, and FastAPI. The purpose of the library is to standardize and simplify data modeling for articles across various applications and systems, ensuring that any changes in data structure are automatically reflected in all services using this library.

## Installation

To install the library, simply run the following command:

```sh
pip install .
```

### Installing Locally
If you want to install the library locally from a GitHub repository, you can use the following command:

```sh
pip install git+https://github.com/nataliagwardjan/article_models_librery
```

## Directory Structure

```article_models_library
├── models/                  # Pydantic models
│   ├── __init__.py          # Package initialization
│   ├── article_nosql_models.py  # NoSQL models
│   ├── article_sql_models.py    # SQL models
│   ├── error_codes.py       # Error codes
│   └── schemas.py           # Schemas
├── tests                    # Tests
├── .venv                    # Virtual environment
├── .gitignore               # Git ignore file
├── README.md                # This file
├── requirements.txt         # Requirements
└── setup.py                 # Project setup
```


## Usage

Importing models:

```python
from models.article_sql_models import ArticleMetadataDBSchema
```
Creating an instance of the model:
```python
article_data = {
    "id": "10.1234/example-doi",
    "title": "Sample Title",
    "authors": "John Doe, Anna Smith",
    "journal": "Science Journal",
    "year": 2023,
    "volume": 10,
    "keywords": "model, article, python"
}

article = ArticleMetadata(**article_data)
```

Data validation:
```python
article = ArticleMetadata(**article_data)
print(article.id)  # Displays the DOI
```
## Tests

To run the tests, use the following command:

```sh
pytest
```

