from dotenv import load_dotenv
import pymongo
import os

load_dotenv()

client = pymongo.MongoClient(os.environ.get('MONGODB_CLIENT'))

db = client['dblecturer']

#collection
chapters_collection = db['chapters']

#insert
# chapters_collection.insert_one({ "name": "John", "address": "Highway 37" })

#read
data = chapters_collection.find_one({'name':'John'})
print(data)