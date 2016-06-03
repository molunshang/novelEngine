import re;
import pymongo;

client = pymongo.MongoClient('127.0.0.1', 27017);
readerDb = client["book"];

if __name__ == "__main__":
    cursor = readerDb["Book"].find();
    repair = re.compile("(.+?)</i>.*");
    with cursor as c:
        for book in c:
            try:
                print(book);
                res = repair.match(book["Author"]);
                reAuthor = res.group(1);
                readerDb["Book"].update({"_id": book["_id"]}, {"$set": {"Author": reAuthor}});
            except Exception as ex:
                print(ex);
    print("Over");
