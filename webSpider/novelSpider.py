import os, re, asyncio, time;
from multiprocessing import Pool, Process;
import link;
from AsyncBaseSpider.spider import spider;
from AsyncBaseSpider.redisQueue import redisQueue;
from setting import *;
from novelConfig import configs;


class novelSpider(spider):
    def __init__(self, link, loop=None):
        queue = redisQueue("linkQueue_" + link.host);
        queue.enqueue({"link": link.link, "host": link.host, "linktype": link.type});
        if loop is None:
            loop = asyncio.get_event_loop();
        spider.__init__(self, queue, os.cpu_count(), loop);
        self.redisClient = redis.Redis(connection_pool=redisPool);
        self.historyName = time.strftime('%y-%m-%d', time.localtime(time.time()));
        self.bookDict = globalBookDict;

    # @staticmethod
    # def beginTransaction():
    #     client=redis.Redis(connection_pool=redisPool);
    #     tranName = "currentTransaction";
    #     tran = client.get(tranName);
    #     if tran is None:
    #         with client.pipeline() as pipe:
    #             try:
    #                 pipe.watch(tranName)
    #                 tranVersion = pipe.incr(tranName + "_version");
    #                 pipe.multi()
    #                 pipe.set(tranName, tranVersion)
    #                 pipe.execute()
    #                 return tranVersion;
    #             except redis.WatchError as e:
    #                 return client.get(tranName);
    #     else:
    #         return tran;
    #
    # def closeTransaction(self):
    #     tranName = "queueTran_" + self.queue.queueName;
    #     self.redisClient.delete(tranName);

    def filter(self, item):
        return redisClient.sismember(self.historyName, item);

    def record(self, item):
        redisClient.sadd(self.historyName, item);

    @asyncio.coroutine
    def parse(self, data, item):
        host = item["host"];
        link = item["link"];
        config = configs[host];
        html = data.decode(config["encoding"], "ignore");
        if not html or len(html) <= 0:
            return;
        linkType = item["linktype"];
        if linkType == 1:
            yield from self.parseLink(html, config, host, link);
        elif linkType == 2:
            yield from self.parseContent(html, config, host, link);
        elif linkType == 3:
            yield from self.parseArticle(html, config, host, link);
        print("抓取链接%s,类型%s" % (link, str(linkType)));

    # @asyncio.coroutine
    # def craw(self):
    #     tran = self.beginTransaction();
    #     self.historyName = self.historyName + "_" + int(tran);
    #     yield from super().craw();
    #     self.closeTransaction();

    @asyncio.coroutine
    def parseLink(self, html, config, host, link):
        '''
        格式化列表
        '''
        regItem = config["list"];
        reg = regItem["regex"];
        time = config["time"];
        linkType = regItem["type"];
        links = re.findall(reg, html);
        times = re.findall(time, html);
        lastTime = redisClient.get("lastTime_" + host);
        if not lastTime:
            lastTime = config["lastTime"];
        elif not isinstance(lastTime, str):
            lastTime = lastTime.decode("utf-8");
        if links:
            for l in set(links):
                nl = self.convertLink(host, l, link, linkType);
                if nl and not self.filter(nl):
                    self.queue.enqueue({"link": nl, "host": host, "linktype": linkType});
        regItem = config["detail"];
        linkType = regItem["type"];
        details = re.findall(regItem["regex"], html);
        if details:
            index = 0;
            for l in set(details):
                if times:
                    tlen = len(times);
                    if index >= tlen:
                        index = tlen - 1;
                    t = times[index];
                    index = index + 1;
                    if t < lastTime:
                        continue;
                nl = self.convertLink(host, l, link, linkType);
                if nl and not self.filter(nl):
                    self.queue.enqueue({"link": nl, "host": host, "linktype": linkType});

    @asyncio.coroutine
    def parseContent(self, html, config, host, link):
        '''
        格式化小说主页
        :param html:
        :param config:
        :param host:
        :param link:
        :return:
        '''
        yield from self.ensureBook(html, config);
        regItem = config["detailList"];
        res = re.findall(regItem["regex"], html);
        if res:
            for l in set(res):
                self.convertLink(host, l, link, regItem["type"]);
                if not self.filter(l):
                    self.queue.enqueue({"link": l, "host": host, "linktype": regItem["type"]});

    @asyncio.coroutine
    def parseArticle(self, html, config, host, link):
        info = yield from self.ensureBook(html, config);
        if not info:
            return
        itemRex = config["detailItem"];
        items = [{"name": t[1], "link": t[0]} for t in re.findall(itemRex, html)];
        if config["itemSort"]:
            items.sort(key=lambda x: x["link"]);
        bookId = info[1]["bookId"];
        order = 1;
        for li in items:
            yield from client["book"].BookLinks.update({"BookId": bookId, "LinkName": li["name"]},
                                                       {"$addToSet": {
                                                           "Links": self.convertLink(host, li["link"], link, 3)},
                                                           "$setOnInsert": {"Time": time.time(), "Num": order}},
                                                       True);
            order = order + 1;
        print("获取小说%s,编号：%d,章节数%d" % (info[0], bookId, order));

    def convertLink(self, host, l, link, type):
        '''
        生成可爬取连接
        :param host:
        :param l:
        :param link:
        :param type:
        :return:
        '''
        if l[0] == "/":
            l = host + l;
        elif l.startswith("http://") or l.startswith("https://"):
            l = l;
        elif link.endswith("/"):
            l = link + l;
        else:
            strl = len(link) - 1;
            while strl > 0 and link[strl] != "/":
                strl = strl - 1;
            if strl > 0:
                l = link[0:strl] + "/" + l;
        return l;

    @asyncio.coroutine
    def ensureBook(self, html, config):
        titleRex = config["title"];
        authorRex = config["author"];
        iconRex = config["icon"];
        title = re.search(titleRex, html);
        if not title:
            return None;
        title = title.group(1) or title.group(2)
        author = re.search(authorRex, html);
        if author:
            author = author.group(1) or author.group(2)
        else:
            author = "";
        icon = re.search(iconRex, html);
        if icon:
            icon = icon.group(0);
        info = self.bookDict.get(title);
        if not info:
            seq = yield from client["book"].GlobalSequence.find_and_modify({"SequenceName": "BookId"},
                                                                           {"$inc": {"SequenceValue": 1}}, True);
            bookId = seq["SequenceValue"];
            res = yield from client["book"].Book.find_and_modify({"BookName": title, "Author": author},
                                                                 {"$set": {"Icon": icon},
                                                                  "$setOnInsert": {"_id": bookId}}, True, new=True);
            bookId = res["_id"];
            info = {"bookId": bookId, "icon": icon}
        elif not info["icon"] and icon and len(icon) > 0:
            yield from client["book"].Book.update({"_id": info["bookId"]}, {"$set": {"Icon": icon}});
            info["icon"] = icon;
        self.bookDict[title] = info;
        return title, info;


def runSpider(link):
    reader = novelSpider(link);
    reader.run();
    now = time.strftime('%y-%m-%d', time.localtime(time.time()));
    redisClient.set("lastTime_" + link.host, now);


if __name__ == "__main__":
    poolSize = min(len(configs), os.cpu_count());
    with Pool(processes=poolSize) as p:
        p.map(runSpider, [link.link(k, 1, k) for k in configs]);
