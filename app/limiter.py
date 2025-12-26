import redis
import time
import os
# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')

r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

def is_allowed(user_id: str, limit: int, window_seconds: int) -> bool:
    """
    Checks if a request is allowed using the Sliding Window algorithm.
    """
    # FIX: Use float (time.time()) instead of int() to capture milliseconds
    current_time = time.time() 
    window_start = current_time - window_seconds

    try:
        # 1. Clean up old requests
        r.zremrangebyscore(user_id, 0, window_start)
        
        # 2. Count current requests
        request_count = r.zcard(user_id)
        
        if request_count < limit:
            # FIX: Use the full timestamp as the unique member ID
            r.zadd(user_id, {str(current_time): current_time})
            r.expire(user_id, window_seconds)
            return True
            
        return False
        
    except redis.RedisError as e:
        print(f"Redis Error: {e}")
        return True