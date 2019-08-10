#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis

# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "localhost"
redis_port = 6379
redis_password = ""


def getRedisObject():
    """Example Hello Redis Program"""
    
    # step 3: create the Redis Connection object
    try:
        print("\nConnecting to redis...")        
        
        # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
        # using the default encoding utf-8.  This is client specific.
        redisConnectionObj = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    
        if(redisConnectionObj is not None):
            return redisConnectionObj
    
        # step 4: Set the hello message in Redis 
        # r.set("msg:hello", "Hello Redis!!!")
        

        # step 5: Retrieve the hello message from Redis
        # msg = r.get("msg:hello")
    
    except Exception as e:
        print(e)
        return None


# if __name__ == '__main__':
#     hello_redis()