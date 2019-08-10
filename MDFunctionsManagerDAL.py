import MDRedis

def sendVideoDataQToRedis(cameraName, VideoDataQStringToRedis):
    redisConnectionObj = MDRedis.getRedisObject()
    
    if(redisConnectionObj is not None):
        print("Set: {}VideoDataQ\n".format(cameraName))
        redisConnectionObj.set("{}VideoDataQ".format(cameraName), VideoDataQStringToRedis)
    else:
        print("DAL Error: Failed sending VideoDataQ to redis.\n")


# sendVideoDataQToRedis(cameraName, VideoDataQStringToRedis)
