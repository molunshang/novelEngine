import redis;
from AsyncBaseSpider.spiderQueue import spiderQueue


class redisQueue(spiderQueue):
    def __init__(self, name, address="127.0.0.1", port=6379):
        self.client = redis.Redis(connection_pool=redis.ConnectionPool(host=address, port=port, db=0));
        self.__queueName__ = name;

    def enqueue(self, item):
        self.client.lpush(self.__queueName__, item);

    def dequeue(self):
        data = self.client.rpop(self.__queueName__);
        if data is not None:
            data = eval(data[1]);
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
