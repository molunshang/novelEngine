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
with cursor as bc:
    for book in bc:
        globalBookDict[book["BookName"]] = {"bookId": book["_id"], "icon": book["Icon"]};

configs = dict();
cursor = syncClient["book"].siteConfigs.find();
with cursor as sc:
    for site in sc:
        configs[site["_id"]] = {
            "encoding": site["SiteEncoding"],
            "list": {"regex": site["ListRegex"], "type": 1},
            "detail": {"regex": site["DetailRegex"],
                       "type": 3 if site["DetailRegex"] == site["DetailListRegex"] else 2},
            "detailList": {"regex": site["DetailListRegex"], "type": 3},
            "title": site["TitleRegex"],
            "author": site["AuthorRegex"],
            "detailItem": site["AuthorRegex"],
            "time": site["ListTimeRegex"],
            "lastTime": site["LastTime"],
            "icon": site["IconRegex"],
            "itemSort": site["ItemSort"]
        };


def addSiteConfig(site):
    configs[site["_id"]] = {
        "encoding": site["SiteEncoding"],
        "list": {"regex": site["ListRegex"], "type": 1},
        "detail": {"regex": site["DetailRegex"], "type": 3 if site["DetailRegex"] == site["DetailListRegex"] else 2},
        "detailList": {"regex": site["DetailListRegex"], "type": 3},
        "title": site["TitleRegex"],
        "author": site["AuthorRegex"],
        "detailItem": site["AuthorRegex"],
        "time": site["ListTimeRegex"],
        "lastTime": site["LastTime"],
        "icon": site["IconRegex"],
        "itemSort": site["ItemSort"]
    };
