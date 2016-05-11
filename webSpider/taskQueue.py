import queue;
import redis;

taskQueue = queue.Queue();
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0);
db = redis.Redis(connection_pool=pool);
visitedUrl = dict();
