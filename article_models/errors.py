from typing import Optional

ERROR_CODES = {
    'AML-0': 'UNDEFINED_ERROR',
    'AML-1': 'INVALID_FIELD',
    'AML-2': 'MISSING_FIELD'
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
