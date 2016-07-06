from flask import blueprints, jsonify, request
from time import time;
from config import *;
from builtins import list as array;

api = blueprints.Blueprint("api", __name__)


@api.route('/search/<name>')
def search(name):
    result = bookDb.Book.find({"BookName": {"$regex": "^(" + name + ")"}});
    return jsonify(isok=True, data=toArray(result));


@api.route('/newbooklist/<float:searchtime>', methods=["get", "post"])
def getNewItem(searchtime):
    searchtime = float(searchtime);
    if "books" not in request.form:
        return jsonify(isok=False, msg="参数错误")
    books = request.form["books"];
    if books is None or books == "":
        return jsonify(isok=False, msg="参数错误")
    bookArray = books.split(",");
    if len(bookArray) <= 0:
        return jsonify(isok=False, msg="参数错误")
    bookArray = array(map(lambda id: int(id), bookArray));
    result = bookDb.BookLinks.find({"BookId": {"$in": bookArray}, "Time": {"$gte": searchtime}});
    return jsonify(isok=True, data=toArray(result), serverTime=time());


@api.route('/list/<int:index>')
def list(index):
    index = int(index) - 1;
    if index < 0:
        index = 0;
    result = bookDb.Book.find().skip(30 * index).limit(30);
    return jsonify(isok=True, data=toArray(result));


@api.route('/detail/<int:bookId>')
def detail(bookId):
    bookId = int(bookId);
    if bookId < 1:
        return jsonify(isok=False);
    result = bookDb.BookLinks.find({"BookId": bookId});
    return jsonify(isok=True, data=toArray(result));


@api.route('/config')
def config():
    result = bookDb.siteConfigs.find({}, {"SiteName": True, "SiteHost": True, "MatchType": True, "DetailMatch": True});
    return jsonify(isok=True, data=toArray(result), serverTime=time());
