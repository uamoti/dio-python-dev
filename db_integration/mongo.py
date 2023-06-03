#!/usr/bin/python3

import json
from pprint import pprint
from pymongo.mongo_client import MongoClient

uri = open('mongo.uri').readline()

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)

# Create DB named blog
db = client.blog
# Create collection named posts
posts = db.posts
#data = json.load(open('posts.json'))
# RUN ONLY ONCE
#result = posts.insert_many(data)
#print("\nINSERT IDS:")
#pprint(result.inserted_ids)

print("\nFIRST POST FROM COLLECTION")
pprint(posts.find_one())

print("\nPOST FROM A SPECIFIC USER:")
pprint(posts.find_one({'user': 'jborrowman2'}))

print("\nPOSTS FROM DIFFERENT USERS:")
results = posts.find({'user': {'$in': ['jborrowman2', 'hdeverock3']}})

for r in results:
    pprint(r)

