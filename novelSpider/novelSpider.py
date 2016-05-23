from flask import Flask;
from flask import jsonify;
from pymongo import mongo_client;

app = Flask(__name__)
client = mongo_client.MongoClient(host='127.0.0.1', port=27017);
bookDb = client["book"];


@app.route('/search/<name>')
def search(name):
    cursor = bookDb.Book.find({"BookName": name});
    return jsonify(isok=True, data=toArray(cursor));


@app.route('/list/<int:index>')
def list(index):
    index = int(index) - 1;
    if index < 0:
        index = 0;
    cursor = bookDb.Book.find().skip(30 * index).limit(30);
    return jsonify(isok=True, data=toArray(cursor));


@app.route('/detail/<int:bookId>')
def detail(bookId):
    bookId = int(bookId);
    if bookId < 1:
        return jsonify(isok=False);
    cursor = bookDb.BookLinks.find({"BookId": bookId});
    return jsonify(isok=True, data=toArray(cursor));


def toArray(cursor):
    result = [];
    try:
        with cursor as c:
            for r in c:
                result.append(r);
    except Exception as e:
        print(e);
    return result;


if __name__ == '__main__':
    app.run(host='192.168.1.78')
