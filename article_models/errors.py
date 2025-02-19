from typing import Optional

SERVER_ERRORS_CODES = {
    'article_models_library': 'AML',
    'database_management_service': 'DMS',
    'article_search_service': 'ASS',
    'article_download_service': 'ADS',
    'article_pdf_management_service': 'APMS',
    'article_summarise_service': 'ASumS'
}

ERROR_CODES = {
    f'{SERVER_ERRORS_CODES['article_models_library']}-0': 'UNDEFINED_ERROR',
    f'{SERVER_ERRORS_CODES['article_models_library']}-1': 'INVALID_FIELD',
    f'{SERVER_ERRORS_CODES['article_models_library']}-2': 'MISSING_FIELD'
}


class CustomError(Exception):
    def __init__(self, error_code: str, error_message: str, additional_info: Optional[str] = ''):
        self.error_code = error_code
        self.error_message = error_message
        self.additional_info = additional_info
        super().__init__(f'{error_code}: {error_message}\n{additional_info}')


class ModelValidationError(CustomError):
    def __init__(self, error_code: str, additional_info: Optional[str] = ''):
        if error_code not in ERROR_CODES:
            raise CustomError('AML-0', ERROR_CODES['AML-0'], f'Unknown error_code {error_code}.')
        error_message = ERROR_CODES[error_code]
        super().__init__(error_code=error_code, error_message=error_message, additional_info=additional_info)
