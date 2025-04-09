from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB Atlas URI
MONGO_URI = "mongodb+srv://notescli_usr:mongodb@notescluster.7afyc.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["notescli"]
collection = db["notes"]

def get_all_notes(user_id):
    """Fetch all notes for a user and convert ObjectId to string."""
    notes = list(collection.find({"user_id": user_id}, {"_id": 1, "title": 1, "content": 1}))
    
    # Convert MongoDB ObjectId to string
    for note in notes:
        note["_id"] = str(note["_id"])
    
    return notes  # Ensure a list of dictionaries is returned

def get_note(user_id, note_id):
    """Fetch a single note by ID and convert ObjectId to string."""
    try:
        note = collection.find_one({"_id": ObjectId(note_id), "user_id": user_id}, {"_id": 1, "title": 1, "content": 1})
        if note:
            note["_id"] = str(note["_id"])
        return note
    except:
        return None

def create_note(user_id, title, content):
    note = {"user_id": user_id, "title": title, "content": content}
    result = collection.insert_one(note)
    return str(result.inserted_id)

def update_note(user_id, note_id, title, content):
    try:
        result = collection.update_one(
            {"_id": ObjectId(note_id), "user_id": user_id},
            {"$set": {"title": title, "content": content}}
        )
        return result.modified_count > 0
    except:
        return False

def delete_note(user_id, note_id):
    try:
        result = collection.delete_one({"_id": ObjectId(note_id), "user_id": user_id})
        return result.deleted_count > 0
    except:
        return False
