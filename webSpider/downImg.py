import os;
import multiprocessing;
from multiprocessing import Queue, Process;
import asyncio;
import aiohttp;

def asyncDownImage(queue):
    @asyncio.coroutine
    def fetch_page(session, proname, url):
        try:
            with aiohttp.Timeout(10):
                response = yield from session.get(url);
                print('异步获取图片：进程 %s,链接 %s' % (proname, link));
                result = (yield from response.read());
                response.close();
                return result;
        except Exception as ex:
            print(ex);
            return None;

    loop = asyncio.get_event_loop();
    pro = multiprocessing.current_process();
    multiprocessing.Pool

    while queue.qsize() > 0:
        try:
            link = queue.get(True, 10);
            pathItems = link.split('/')[3:];
            path = 'images\\' + '\\'.join(pathItems);
            if os.path.exists(path):
                continue;
            dirpath = os.path.dirname(path);
            if not os.path.exists(dirpath):
                os.makedirs(dirpath);
            with aiohttp.ClientSession(loop=loop) as session:
                data = loop.run_until_complete(fetch_page(session, pro.name, link));
            if data is None:
                queue.put(link);
                continue;
            with open(path, 'wb') as saver:
                saver.write(data);
        except Exception as ex:
            print(ex);


if __name__ == "__main__":
    qu = Queue();
    jobs = [];
    for i in range(0, 8):
        p = Process(target=asyncDownImage, args=(qu,));
        jobs.append(p);
        p.start();
    with open('imgs.txt', 'r', encoding='utf8') as reader:
        lines = reader.readlines();
        for l in lines:
            temp = l.split('   ');
            link = temp[0][5:];
            qu.put(link);
    for p in jobs:
        p.join();
    print("img get over");
