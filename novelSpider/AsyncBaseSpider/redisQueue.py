import redis;
from AsyncBaseSpider.spiderQueue import spiderQueue
import setting;


class redisQueue(spiderQueue):
    def __init__(self, name):
        self.client = redis.Redis(connection_pool=setting.redisPool);
        self.__queueName__ = name;

    def enqueue(self, item):
        self.client.lpush(self.__queueName__, item);

    def dequeue(self):
        data = self.client.rpop(self.__queueName__);
        if data is not None:
            data = eval(data);
        return data;

    def blockDequeue(self):
        data = self.client.brpop(self.__queueName__);
        if data is not None:
            data = eval(data);
        return data;

    def count(self):
        return self.client.llen(self.__queueName__);

    @property
    def queueName(self):
        return self.__queueName__;
