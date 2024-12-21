import json
import random
import os
from datetime import datetime, timedelta

ADMIN_FILE = "admin.json"
USERS_FILE = "users.json"

## Styling
def wait(): input("\nPress ENTER to Continue... ")
def fresh(): print("\n" * 50) #os.system('cls' if os.name == 'nt' else 'clear')
#####

## Loading JSON files
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
#####

## Searching for users
def search_user(database, attribute, search_term):
    if attribute == '1': # Search by ID
       if search_term in database:
           return {"id": search_term, **database[search_term]}

    elif attribute == '2': # Search by Phone Number
        for user_id in database:
            user = database[user_id]
            if search_term == user['phone']:
                return {"id": user_id, **database[user_id]}

    elif attribute == '3': # Search by username
        for user_id in database:
            user = database[user_id]
            if search_term.lower() == user['username'].lower():
                return {"id": user_id, **database[user_id]}

    return None
#############