import pymongo
from datetime import datetime, timedelta

# Configure MongoDB
connection = pymongo.MongoClient('mongodb://localhost:27017')
db = connection['TMA']

#collection: trolley
def create_recording(name, date, temp): #str, dateobj, int
    assert name is not None
    assert date is not None
    assert temp is not None

    db.trolley.insert_one({"name":name, "date":date, "temp":temp})

def find_all(): #for the recordings creation page
    return db.trolley.find({}).sort("date", -1) #find latest inserted date

