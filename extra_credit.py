import pprint
import pymongo

connection = pymongo.MongoClient("class-mongodb.cims.nyu.edu", 27017,
                                username="yw6157",
                                password="heH7egqr",
                                authSource="yw6157")
collection = connection["yw6157"]["listings"]

query = {
    "beds": {"$gt": 2},
    "neighbourhood_group_cleansed":'Brooklyn'
}
projection = {
    "_id": 0,
    "name": 1,
    "beds": 1,
    "review_scores_rating": 1,
    "price": 1
}

results = collection.find(query, projection).sort("review_scores_rating", -1)

for document in results:
    pprint.pprint(document)