import pymongo;

client = pymongo.MongoClient('127.0.0.1', 27017);
readerDb = client["book"];

if __name__ == "__main__":
    cursor = readerDb["write"].find().limit(1)
    for book in cursor:
        try:
            seq = readerDb["GlobalSequence"].find_and_modify({"SequenceName": "BookId"},
                                                             {"$inc": {"SequenceValue": 1}}, True);
            bookId = seq["SequenceValue"];
            res=readerDb["Book"].update({"BookName": book["bookName"], "Author": book["author"]}, {"$set": {"_id": bookId,
                                                                                                        "Icon": ""}},
                                    True);
            print(res);
            links = list();
            order = 1;
            for link in book["links"]:
                l = {"BookId": bookId, "LinkName": link["name"], "Links": [book["baselink"] + link["link"]],
                     "Num": order};
                links.append(l);
                order = order + 1;
            readerDb["BookLinks"].insert(links)
            print(book["bookName"]);
        except Exception as ex:
            print(ex);
    print("Over");
