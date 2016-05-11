import asyncio;
import motor.motor_asyncio
import taskQueue
import re;
import aiohttp, base64, json;
from bson import objectid;

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017);
db = client['blog_database'];
img = re.compile('"(http://static.open-open.com/lib/uploadImg/.+?)"');


@asyncio.coroutine
def insertData(col, doc):
    result = yield from col.insert(doc);
    print(result);


@asyncio.coroutine
def loopWrite(col):
    while True:
        try:
            doc = taskQueue.db.rpop("articles");
            if doc == None:
                return;
            yield from insertData(col, eval(doc));
        except Exception as ex:
            taskQueue.db.lpush("articles", doc);
            print(ex);


@asyncio.coroutine
def initTaskQueue():
    cursor = db.blogs.find();
    while (yield from cursor.fetch_next):
        document = cursor.next_object()
        document["_id"] = str(document["_id"]);
        taskQueue.db.lpush("downImage", document);


@asyncio.coroutine
def downImage(url):
    with aiohttp.ClientSession() as session:
        with aiohttp.Timeout(10):
            response = yield from session.get(url);
            print('获取图片：链接 %s' % url);
            result = (yield from response.read());
            response.close();
            return "data:image/png;base64," + base64.b64encode(result).decode("utf-8");


@asyncio.coroutine
def syncImage():
    while True:
        try:
            doc = taskQueue.db.rpop("downImage");
            if doc == None:
                return;
            document = eval(doc);
            document["_id"] = objectid.ObjectId(document["_id"]);
            document["images"] = list();
            c = document["content"];
            res = img.findall(c);
            if res:
                for link in res:
                    document["images"].append(link);
                    strImage = yield from downImage(link);
                    document["content"] = c.replace(link, strImage);
                yield from db.blogs.save(document);
        except Exception as ex:
            taskQueue.db.lpush("downImage", doc);
            print(ex);


if __name__ == "__main__":
    article = db["blogs"];
    loop = asyncio.get_event_loop();
    # loop.run_until_complete(asyncio.wait([loopWrite(article), loopWrite(article), loopWrite(article)]));
    # loop.run_until_complete(initTaskQueue());
    loop.run_until_complete(asyncio.wait([syncImage(), syncImage(), syncImage()]));
