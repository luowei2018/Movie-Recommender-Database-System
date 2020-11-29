from flask import Flask
import pymongo
# from insertToMongo import outputJson
import insertToMongo
# import db
mongo = Flask(__name__)
@mongo.route('/')
def cluster0():
    return "flask mongodb atlas!"

@mongo.route('/test')
def test():
    print("i'm here")
    CONNECTION_STRING = "mongodb+srv://shirui:pig@cluster0.hckie.mongodb.net/users?retryWrites=true&w=majority"
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client.users
    print(db.users_flask.count_documents({}))
    try:
        movies = insertToMongo.outputJson()
        # print(movies)
        db.users_flask.insert_many(movies)
    except Exception as e:
        print(e)
    return "Connected to the data base!"

if __name__ == '__main__':
    mongo.run(port=8000)
    # mongo.debug = True
#test to insert data to the data base

