import logging
import sys
import json
from datetime import datetime, timezone


import logging
import json
import sys
from datetime import datetime, timezone
from errors import SERVICE_CODES

class JSONFormatter(logging.Formatter):
    def __init__(self, service_name: str):
        super().__init__()
        self.service_code = SERVICE_CODES.get(service_name, 'UNKNOWN')

    def format(self, record):
        log_record = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': f'{self.service_code}/{record.module}',
            'function': record.funcName,
            'line': record.lineno,
        }
        if record.exc_info:
            exception_info = self.formatException(record.exc_info)
            log_record['exception'] = {
                'number_of_errors': len(getattr(record, 'extra_errors', [])),
                'detail': getattr(record, 'extra_errors', exception_info)
            }
        return json.dumps(log_record, ensure_ascii=False)

def setup_logger(service_name: str) -> logging.Logger:
    service_code = SERVICE_CODES.get(f'{service_name}', 'UNKNOWN')  
    logger = logging.getLogger(service_code)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter(f'{service_name}'))

    logger.addHandler(handler)
    return logger
