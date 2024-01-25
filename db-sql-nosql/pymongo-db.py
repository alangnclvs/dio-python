# Import necessary PyMongo modules
import pymongo
import pprint
import datetime

# Define constants for MongoDB credentials
USERNAME = "Enter your username here"
PASSWORD = "Enter your password here"

# Connect to MongoDB Atlas
try:
    client = pymongo.MongoClient(
        f"mongodb+srv://{USERNAME}:{PASSWORD}@"
        "pymongo-dio.prxhaoz.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client.test
    posts = db.posts
    print("Connected to MongoDB Atlas")
except pymongo.errors.ConnectionFailure:
    print("Connection to MongoDB Atlas failed")
    exit()

# Insert data into MongoDB
post = {
        "author": "Alan Gonçalves",
        "text": "My first post on MongoDB",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()
    }

# Insert the post into the posts collection
post_id = posts.insert_one(post).inserted_id
print("Post ID: ", post_id)


# Retrieve data from MongoDB
print("\nRetrieving data from MongoDB")
pprint.pprint(posts.find_one())

# Insert two new posts into the posts collection
new_posts = [
    {
        "author": "Alan Gonçalves",
        "text": "My second post on MongoDB",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()
    },
    {
        "author": "Alan Gonçalves",
        "text": "My third post on MongoDB",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime(1995, 12, 25, 12, 0)
    }
]

# Insert the new posts into the posts collection
result = posts.insert_many(new_posts)
print("Post IDs inserted by insert_many: ", result.inserted_ids)

# Retrieve data from MongoDB by author
print("\nRetrieving data by author (Alan Gonçalves):")
pprint.pprint(posts.find_one({"author": "Alan Gonçalves"}))

# Retrieve all documents from the posts collection
print("\nDocuments present in the posts collection.")
for post in posts.find():
    pprint.pprint(post)
