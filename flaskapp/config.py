# application configuration
import os

config = {
    'FLASK_APP_SECRET': os.environ.get('FLASK_APP_SECRET', ''),
    'DATABASE_NAME': os.environ.get('DATABASE_NAME', ''),
    'DATABASE_HOST': os.environ.get('DATABASE_HOST', ''),
    'DATABASE_USERNAME': os.environ.get('DATABASE_USERNAME',''),
    'DATABASE_PASSWORD': os.environ.get('DATABASE_PASSWORD','',),
}

