from multiprocessing import Pool, Process;
import threading;
import asyncio
import link;
import os
import re
import time
import copy
from AsyncBaseSpider.redisQueue import redisQueue
from AsyncBaseSpider.spider import spider
from setting import *;


class novelSpider(spider):
    def __init__(self, link, loop=None):
        self.redisClient = redisClient;
        self.expireKeys = set();
        self.sequenceName = "SeqSpider_" + link.host;
        self.sequence = str(self.getTaskSequence());
        queue = redisQueue("linkQueue_" + link.host);
        queue.enqueue({"link": link.link, "host": link.host, "linktype": link.type, "partitionFlag": self.sequence});
        if loop is None:
            loop = asyncio.get_event_loop();
        spider.__init__(self, queue, os.cpu_count(), loop);

    def getTaskSequence(self):
        taskSeqName = self.sequenceName;
        tran = self.redisClient.get(taskSeqName);
        if tran is None:
            rawSeq = self.redisClient.get("Sequence_" + taskSeqName);
            if (rawSeq is None):
                seq = 1;
            else:
                seq = int(rawSeq) + 1;
            with self.redisClient.pipeline() as pipe:
                try:
                    pipe.watch(taskSeqName);
                    pipe.multi();
                    pipe.set(taskSeqName, seq);
                    pipe.set("Sequence_" + taskSeqName, seq);
                    pipe.execute();
                    return seq;
                except redis.WatchError as e:
                    return int(self.redisClient.get(taskSeqName));
        else:
            return int(tran);

    def closeTransaction(self):
        self.redisClient.delete(self.sequenceName);
        for k in self.expireKeys:
            self.redisClient.expire(k, 3600 * 24 * 3);

    def filter(self, item):
        recordName = "record_" + item["host"] + "_" + item["partitionFlag"];
        self.expireKeys.add(recordName);
        return redisClient.sismember(recordName, item["link"]);

    def record(self, item):
        recordName = "record_" + item["host"] + "_" + item["partitionFlag"];
        self.expireKeys.add(recordName);
        redisClient.sadd(recordName, item["link"]);

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
            yield from self.parseLink(html, config, item);
        elif linkType == 2:
            yield from self.parseContent(html, config, item);
        elif linkType == 3:
            yield from self.parseArticle(html, config, item);
        print("抓取链接%s,类型%s" % (link, str(linkType)));

    @asyncio.coroutine
    def parseLink(self, html, config, linkItem):
        '''
        格式化列表
        '''
        canBreak = self.paresInfo(html, config, linkItem);
        if canBreak:
            return;
        self.parseList(html, config, linkItem);

    def parseList(self, html, config, linkItem):
        dataItem = copy.deepcopy(linkItem);
        host = linkItem["host"];
        preLink = linkItem["link"];
        regItem = config["list"];
        linkType = regItem["type"];
        reg = regItem["regex"];
        links = re.findall(reg, html);
        if links:
            for l in set(links):
                nl = self.convertLink(host, l, preLink, linkType);
                if nl:
                    dataItem["link"] = nl;
                    dataItem["linktype"] = linkType;
                    if not self.filter(dataItem):
                        self.queue.enqueue(dataItem);

    def paresInfo(self, html, config, linkItem):
        dataItem = copy.deepcopy(linkItem);
        listFlag = True;
        host = linkItem["host"];
        regItem = config["detail"];
        time = config["time"];
        preLink = linkItem["link"];
        lastTime = redisClient.get("lastTime_" + host);
        if not lastTime:
            lastTime = config["lastTime"];
        elif not isinstance(lastTime, str):
            lastTime = lastTime.decode("utf-8");
        linkType = regItem["type"];
        times = re.findall(time, html);
        details = set(re.findall(regItem["regex"], html));
        if (not details or len(details) <= 0) or (not times or len(times) <= 0):
            return False;
        if details:
            timeLastIndex = len(times) - 1;
            index = 0;
            for l in details:
                dataItem["partitionFlag"] = times[min(index, timeLastIndex)];
                if dataItem["partitionFlag"] < lastTime:
                    continue;
                listFlag = False;
                index = index + 1;
                nl = self.convertLink(host, l, preLink, linkType);
                if nl:
                    dataItem["link"] = nl;
                    dataItem["linktype"] = linkType;
                    if not self.filter(dataItem):
                        self.queue.enqueue(dataItem);
        return listFlag;

    @asyncio.coroutine
    def parseContent(self, html, config, linkItem):
        '''
        格式化小说主页
        :param html:
        :param config:
        :param host:
        :param link:
        :return:
        '''
        dataItem = copy.deepcopy(linkItem);
        yield from self.ensureBook(html, config);
        regItem = config["detailList"];
        res = re.findall(regItem["regex"], html);
        if res:
            for l in set(res):
                dataItem["link"] = self.convertLink(dataItem["host"], l, dataItem["link"], regItem["type"]);
                dataItem["linktype"] = regItem["type"];
                if not self.filter(dataItem):
                    self.queue.enqueue(dataItem);

    @asyncio.coroutine
    def parseArticle(self, html, config, linkItem):
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
                                                           "Links": self.convertLink(linkItem["host"], li["link"],
                                                                                     linkItem["link"], 3)},
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
        title = (title.group(1) or title.group(2)).strip()
        author = re.search(authorRex, html);
        if author:
            author = (author.group(1) or author.group(2)).strip()
        else:
            author = "";
        icon = re.search(iconRex, html);
        if icon:
            icon = icon.group(0);
        infoKey = "book:" + title + "_" + author;
        info = self.redisClient.get(infoKey);
        if info is not None:
            info = eval(info);
        change = False;
        if not info:
            seq = yield from client["book"].GlobalSequence.find_and_modify({"SequenceName": "BookId"},
                                                                           {"$inc": {"SequenceValue": 1}}, True);
            bookId = seq["SequenceValue"];
            res = yield from client["book"].Book.find_and_modify({"BookName": title, "Author": author},
                                                                 {"$set": {"Icon": icon},
                                                                  "$setOnInsert": {"_id": bookId}}, True, new=True);
            bookId = res["_id"];
            info = {"bookId": bookId, "icon": icon}
            change = True;
        elif (not info["icon"] or info["icon"] is None) and icon and len(icon) > 0:
            yield from client["book"].Book.update({"_id": info["bookId"]}, {"$set": {"Icon": icon}});
            info["icon"] = icon;
            change = True;
        if change:
            self.redisClient.set(infoKey, info, ex=60 * 3);
        return title, info;


def runSpider(link):
    reader = novelSpider(link);
    reader.run();
    reader.closeTransaction();
    now = time.strftime('%y-%m-%d', time.localtime(time.time()));
    redisClient.set("lastTime_" + link.host, now);


def run():
    poolSize = min(len(configs), os.cpu_count());
    p = Pool(processes=poolSize);
    for l in [link.link(k, 1, k) for k in configs]:
        p.apply_async(runSpider, args=(l,));
    p.close();
    p.join();


def watch():
    siteQueue = redisQueue("spiderSite");
    while 1:
        site = siteQueue.blockDequeue();
        if site is not None:
            addSiteConfig(site);
            l = link.link(site["_id"], 1, site["_id"]);
            p = Process(target=runSpider, args=(l,));
            p.start();


if __name__ == "__main__":
    t = threading.Thread(target=watch);
    t.start();
    while True:
        run();
        print("抓取结束");
        time.sleep(60 * 60 * 3);
