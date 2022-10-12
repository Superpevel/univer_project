import os
import pathlib
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = pathlib.Path().resolve()

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s : %(asctime)s] %(message)s'
        }
    },
    'handlers': {
        'stream_handler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
        'file_handler': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 100000000,
            'backupCount': 10,
            'formatter': 'default_formatter',
            'filename': os.environ.get('LOG_FILE_INFO'),
        }
    },
    'loggers': {
        '': {
            'handlers': ['stream_handler', 'file_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}