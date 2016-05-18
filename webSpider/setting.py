import redis;
import motor.motor_asyncio
import pymongo;

redisHost = "127.0.0.1";
port = 6379;
redisPool = redis.ConnectionPool(host=redisHost, port=port, db=0);
redisClient = redis.Redis(connection_pool=redisPool);

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017);
syncClient = pymongo.MongoClient('127.0.0.1', 27017)

globalBookDict = dict();
cursor = syncClient["book"].Book.find();
for book in cursor:
    globalBookDict[book["BookName"]] = {"bookId": book["_id"], "icon": book["Icon"]};
