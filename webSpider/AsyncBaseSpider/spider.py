import asyncio;
import aiohttp;


class spider(object):
    requestHeader = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER'};
    records = set([]);

    def __init__(self, queue, concurrentCount=3, loop=None):
        self.queue = queue;
        if loop is None:
            loop = asyncio.get_event_loop();
        self.loop = loop;
        self.concurrent = concurrentCount;

    @asyncio.coroutine
    def get(self, url, out=None):
        with aiohttp.ClientSession(loop=self.loop, headers=self.requestHeader) as session:
            with aiohttp.Timeout(10 if out is None else out):
                response = yield from session.get(url);
                result = yield from response.read();
                response.close();
                return response.status, result;

    @asyncio.coroutine
    def parse(self, data, item):
        pass;

    def filter(self, item):
        return item in spider.records;

    def record(self, item):
        spider.records.add(item);

    @asyncio.coroutine
    def craw(self):
        try:
            while True:
                try:
                    item = self.queue.dequeue();
                    if item is None:
                        return;
                    if self.filter(item):
                        continue;
                    timeOut = item["timeout"] if "timeout" in item else 1;
                    data = yield from self.get(item["link"], timeOut * 10);
                    if data[0] == 200:
                        yield from self.parse(data[1], item);
                        self.record(item);
                except Exception as ex:
                    if ex is TimeoutError:
                        outTimes = (item["timeout"] if "timeout" in item else 1) + 1;
                        item["timeout"] = outTimes;
                    self.queue.enqueue(item);
                    print("错误类型:%s,错误信息:%s，链接:%s" % (type(ex), ex, item));
        except Exception as ex:
            print("错误信息:%s" % ex);

    def run(self):
        tasks = [self.craw() for i in range(self.concurrent)];
        self.loop.run_until_complete(asyncio.wait(tasks));

    def runAsync(self):
        return [self.craw() for i in range(self.concurrent)];
