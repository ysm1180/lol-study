import redis
from django.conf import settings

REDIS_CONNECTION_POOL = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)