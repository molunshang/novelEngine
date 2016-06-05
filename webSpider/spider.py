import re;
import pymongo;

client = pymongo.MongoClient('127.0.0.1', 27017);
readerDb = client["book"];

if __name__ == "__main__":
    cursor = readerDb["Book"].find({"BookName": {"$regex": " $"}});
    with cursor as c:
        for book in c:
            try:
                name = book["BookName"].strip();
                same = readerDb["Book"].find_one({"BookName": name});
                if same is not None:
                    links = readerDb["BookLinks"].find({"BookId": book["_id"]});
                    with links:
                        for l in links:
                            readerDb["BookLinks"].update({"BookId": same["_id"], "LinkName": l["LinkName"]},
                                                         {"$addToSet": {
                                                             "Links": {"$each": l["Links"]}}
                                                         });
                    if same["Icon"] is None:
                        same["Icon"] = book["Icon"];
                        readerDb["Book"].update(same);
                    readerDb["BookLinks"].remove({"BookId": book["_id"]});
                    readerDb["Book"].remove(book);
                    print("%s-%d-%d" % (name, book["_id"], same["_id"]));
                else:
                    book["BookName"] = name;
                    readerDb["Book"].save(book);
                    print(book["BookName"]);
            except Exception as ex:
                print("error" + ex);
    print("Over");
