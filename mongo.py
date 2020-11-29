from flask import Flask
import pymongo
# import db
mongo = Flask(__name__)
@mongo.route('/')
def cluster0():
    return "flask mongodb atlas!"

@mongo.route('/test')
def test():
    print("i'm here")
    CONNECTION_STRING = "mongodb+srv://luowei:1124@cluster0.hckie.mongodb.net/users?retryWrites=true&w=majority"
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.users
    print(db.users_flask.count_documents({}))
    try:
        db.users_flask.insert_one({"name": "John"})
    except:
        print("something is wrong")
    return "Connected to the data base!"

if __name__ == '__main__':
    mongo.run(port=8000)
#test to insert data to the data base

