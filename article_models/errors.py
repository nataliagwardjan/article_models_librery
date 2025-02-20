from typing import Optional

SERVICE_CODES = {
    'article_analyser_api': 'AAA',
    'article_models_library': 'AML',
    'database_management_service': 'DMS',
    'article_search_service': 'ASS',
    'article_download_service': 'ADS',
    'article_pdf_management_service': 'APMS',
    'article_summarise_service': 'ASumS'
}

ERROR_CODES = {
    f'{SERVICE_CODES['article_analyser_api']}-0': 'UNDEFINED_ERROR',
    f'{SERVICE_CODES['article_models_library']}-0': 'UNDEFINED_ERROR',
    f'{SERVICE_CODES['article_models_library']}-1': 'PYDANTIC_VALIDATION_ERROR'
}


class ArticleAnalyserApiBaseException(Exception):
    def __init__(self, error_code: str, error_message: str, http_status_code: int = 400,
                 additional_info: Optional[str] = ''):
        self.error_code = error_code
        self.error_message = error_message
        self.http_status_code = http_status_code
        self.additional_info = additional_info
        super().__init__(
            f'{self.error_code}: {self.error_message}\n{self.additional_info}. \nHttp status code {self.http_status_code}')


class ModelValidationException(ArticleAnalyserApiBaseException):
    def __init__(self, error_code: str, http_status_code: int = 400, additional_info: Optional[str] = ''):
        if error_code not in ERROR_CODES:
            raise ArticleAnalyserApiBaseException(error_code=f'{SERVICE_CODES['article_analyser_api']}-0',
                                                  error_message=ERROR_CODES[
                                                      f'{SERVICE_CODES['article_analyser_api']}-0'],
                                                  http_status_code=500,
                                                  additional_info=f'Unknown error_code {error_code}. Error code not in ERROR_CODES in article_models_library')
        error_message = ERROR_CODES[error_code]
        super().__init__(error_code=error_code, error_message=error_message, http_status_code=http_status_code,
                         additional_info=additional_info)
