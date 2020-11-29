from flask import Flask
import pymongo
import mongo
CONNECTION_STRING = "mongodb+srv://luowei:1124@cluster0.hckie.mongodb.net/users?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.users
# user_collection = pymongo.collection.Collection(db, 'user_collection')