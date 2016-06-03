from flask import *;
from flask_bootstrap import Bootstrap;
from pymongo import mongo_client;
from AsyncBaseSpider import redisQueue;
from config import *;
import forms;
import api;

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdjflasdjfasdf31241234234ljks";
app.register_blueprint(api.api, url_prefix="/api");
Bootstrap(app);


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


@app.after_request
def makecross(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    response.headers['Access-Control-Allow-Headers'] = allow_headers
    return response


if __name__ == '__main__':
    app.debug = True;
    app.run(host='0.0.0.0')
