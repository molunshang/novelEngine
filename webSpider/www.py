import re;
import taskQueue;
import asyncio;
import aiohttp;
import pickle;

requestHeader = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'};


@asyncio.coroutine
def get(loop, url):
    with aiohttp.ClientSession(loop=loop, headers=requestHeader) as session:
        with aiohttp.Timeout(10):
            response = yield from session.get(url);
            result = yield from response.read();
            response.close();
            return response.status, result;


def post(loop, url, data):
    with aiohttp.ClientSession(loop=loop, headers=requestHeader) as session:
        with aiohttp.Timeout(10):
            response = yield from session.post(url, data=data);
            result = yield from response.read();
            response.close();
            return response.status, result;


@asyncio.coroutine
def readPage(loop, url):
    res = yield from get(loop, url);
    if (res[0] != 200):
        return None;
    return res[1].decode('utf-8');


def parseLink(html):
    listRegex = re.compile('(/lib/list/\d+(\?pn=\d+){0,1})');
    itemRegex = re.compile('(/lib/view/(\S+).html)');
    result = listRegex.findall(html);
    # 列表
    [taskQueue.db.sadd('waitUrls', dict({"link": 'http://www.open-open.com' + r[0], "type": 1})) for r in result];
    items = itemRegex.findall(html);
    # 文章
    [taskQueue.db.sadd('waitUrls', dict({"link": 'http://www.open-open.com' + r[0], "type": 2})) for r in items if
     not taskQueue.db.sismember('visitedUrl',  'http://www.open-open.com' + r[0])];


def parseContent(html):
    titleRegex = re.compile('<h1 id="articleTitle" >(.+)?</h1>');
    topicRegex = re.compile('<a href="/lib/list/[a-z0-9]+">(.+)?</a>');
    tagRegex = re.compile('<a href="/lib/tag/.+?">(.+)?</a>');
    content = re.compile(
        '(<div id="readercontainer"  class="col-md-9">\s+<article>[\s\S]+</article>\s+(<div class="gitinfo" style="margin:15px 0;"></div>){0,1}\s+</div>)');
    article = dict();
    article["title"] = titleRegex.search(html).group(1);
    article["topic"] = [t for t in topicRegex.findall(html)];
    article["tag"] = [t for t in tagRegex.findall(html)];
    article["content"] = content.search(html).group(0);
    taskQueue.db.lpush("articles", article);


@asyncio.coroutine
def crawSite(loop):
    while True:
        try:
            item = taskQueue.db.spop('waitUrls');
            if item == None:
                return;
            item = eval(item);
            link = item["link"];
            type = item["type"];
            if type == 2 and taskQueue.db.sismember('visitedUrl', link):
                continue;
            print("抓取连接%s" % link);
            html = yield from readPage(loop, link);
            if (type == 1):
                parseLink(html);
            elif type == 2:
                parseContent(html);
            taskQueue.db.sadd('visitedUrl', link);
        except Exception as ex:
            taskQueue.db.sadd('waitUrls', item);
            taskQueue.db.sadd('errorHtml', html);
            print("%s--%s" % (ex, link));


class linkItem(object):
    def __init__(self, link, type):
        self.link = link;
        self.type = type;


class detailItem(object):
    def __init__(self, topic, title, content, tags):
        self.topic = topic;
        self.title = title;
        self.content = content;
        self.tags = tags;


if __name__ == "__main__":
    taskQueue.db.sadd('waitUrls', {"link": "http://www.open-open.com/lib/list/all", "type": 1});
    loop = asyncio.get_event_loop();
    loop.run_until_complete(asyncio.wait([crawSite(loop), crawSite(loop), crawSite(loop)]));  #
