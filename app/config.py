import logging
import os

APP_NAME = 'Demo-API'
DEBUG = os.getenv('ENVIRONEMENT') == 'DEV'
APPLICATION_ROOT = os.getenv('APPLICATION_APPLICATION_ROOT', '/application')
HOST = os.getenv('APPLICATION_HOST')
PORT = int(os.getenv('APPLICATION_PORT', '3000'))

aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
KEY = os.getenv('AWS_KEY')
BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

QUEUE_HOST = os.getenv('QUEUE_HOST')
QUEUE_USER_NAME = os.getenv('QUEUE_USER_NAME')
QUEUE_PASSWORD = os.getenv('QUEUE_PASSWORD')
QUEUE_PORT = os.getenv('QUEUE_PORT')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST')

PUBLISH_QUEUE_NAME = os.getenv('PUBLISH_QUEUE_NAME')
SUBSCRIBE_QUEUE_NAME = os.getenv('SUBSCRIBE_QUEUE_NAME')

PUBLISH_QUEUE_EXCHANGE_NAME = os.getenv('PUBLISH_QUEUE_EXCHANGE_NAME')
SUBSCRIBE_QUEUE_EXCHANGE_NAME = os.getenv('SUBSCRIBE_QUEUE_EXCHANGE_NAME')

PUBLISH_QUEUE_EXCHANGE_TYPE = os.getenv('PUBLISH_EXCHANGE_TYPE')
SUBSCRIBE_QUEUE_EXCHANGE_TYPE = os.getenv('SUBSCRIBE_EXCHANGE_TYPE')

PUBLISH_ROUTE_KEY = os.getenv('PUBLISH_ROUTE_KEY')
SUBSCRIBE_ROUTE_KEY = os.getenv('SUBSCRIBE_ROUTE_KEY')

ERROR_QUEUE_EXCHANGE_TYPE = os.getenv('ERROR_QUEUE_EXCHANGE_TYPE')
ERROR_QUEUE_EXCHANGE_NAME = os.getenv('ERROR_QUEUE_EXCHANGE_NAME')
ERROR_QUEUE_NAME = os.getenv('ERROR_QUEUE_NAME')
ERROR_ROUTE_KEY = os.getenv('ERROR_ROUTE_KEY')

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG,
    format='%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s',
    datefmt='%d/%m/%y %H:%M:%S',
)
