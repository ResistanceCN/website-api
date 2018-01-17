import ssl

DEBUG = False
HOST = 'localhost'
PORT = 5000

# Connect via TCP only when REDIS_UNIX_SOCK is None
REDIS_UNIX_SOCK = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

REDIS_AUTH = None
REDIS_DB = 0

REDIS_SSL = False
REDIS_SSL_CERT = None
REDIS_SSL_KEY = None
REDIS_SSL_CA_CERT = None
REDIS_SSL_CERT_REQS = ssl.CERT_REQUIRED  # or ssl.CERT_OPTIONAL or ssl.CERT_NONE

POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_DBNAME = 'cantonres'
POSTGRES_USER = 'ada'
POSTGRES_PASSWORD = 'secret'

GOOGLE_CLIENT_ID='xxx.apps.googleusercontent.com'
GOOGLE_MAP_KEY='xxx'
