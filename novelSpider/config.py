from pymongo import mongo_client, cursor;
from bson import ObjectId;
from AsyncBaseSpider import redisQueue;

client = mongo_client.MongoClient(host='127.0.0.1', port=27017);
bookDb = client["book"];
siteQueue = redisQueue.redisQueue("spiderSite");


def toArray(mcursor):
    """
    转换mongodb查询游标为数组集合
    :param cursor: 查询游标
    :return: 集合
    """
    if not isinstance(mcursor, cursor.Cursor):
        raise TypeError("argument is not " + type(cursor.Cursor))
    result = [];
    try:
        with mcursor as c:
            for r in c:
                if r["_id"] is not None and isinstance(r["_id"], ObjectId):
                    r["_id"] = str(r["_id"]);
                result.append(r);
    except Exception as e:
        print(e);
    return result;
