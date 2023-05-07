import aioredis
from src import config


redis = aioredis.from_url(config.REDIS_DSN, 
                          decode_responses=True) if config.REDIS_DSN else aioredis.Redis(host='redis', 
                                                                                         decode_responses=True)