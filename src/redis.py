import aioredis


redis = aioredis.Redis(host='redis', decode_responses=True)
