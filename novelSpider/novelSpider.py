from flask import Flask
from pymongo import mongo_client;

app = Flask(__name__)
client = mongo_client.MongoClient(host='127.0.0.1', port=27017)
db = client["book"];


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
