import redis;
from AsyncBaseSpider.spiderQueue import spiderQueue
import setting;


class redisQueue(spiderQueue):
    def __init__(self, name):
        self.client = redis.Redis(connection_pool=setting.redisPool);
        self.queueName = name;

    def enqueue(self, item):
        self.client.lpush(self.queueName, item);

    def dequeue(self):
        data = self.client.rpop(self.queueName);
        if data is not None:
            data = eval(data);
        return data;

    def count(self):
        return self.client.llen(self.queueName);
