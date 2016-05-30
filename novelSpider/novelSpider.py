from flask import *;
from flask_bootstrap import Bootstrap;
from pymongo import mongo_client;
from AsyncBaseSpider import redisQueue;
import forms;

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdjflasdjfasdf31241234234ljks";
Bootstrap(app);
client = mongo_client.MongoClient(host='127.0.0.1', port=27017);
bookDb = client["book"];
siteQueue = redisQueue.redisQueue("spiderSite");


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


@app.route('/')
def index():
    return render_template("index.html");


@app.route('/siteconfig/list')
def siteList():
    configs = bookDb.siteConfigs.find();
    return render_template("sitelist.html", sites=configs);


@app.route('/siteconfig/add', methods=["get", "post"])
def siteItem():
    config = forms.siteConfigForm();
    if request.method == "GET":
        return render_template("siteItem.html", form=config);
    if config.validate():
        data = config.data;
        data["_id"] = data["SiteHost"];
        bookDb.siteConfigs.save(data);
        siteQueue.enqueue(data);
        return redirect(url_for("siteList"));

    return redirect(url_for("siteItem"));


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
    app.debug = True;
    app.run(host='0.0.0.0')
