import os
from google.cloud import firestore
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

os.environ['GOOGLE_CLOUD_PROJECT'] = 'tesis-405201'

# Now initialize the Firestore client
db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user_by_id(user_id):
    return db.collection('users').document(user_id).get()

def user_put_data(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({ 'password':user_data.password,
                  'email':user_data.email,
                  'phone': user_data.phone })

def delete_user_by_id(user_id):
    user_ref = get_user_ref(user_id)
    user_ref.delete()
   
def get_user_ref(user_id):
    return db.collection('users').document(user_id)    

def update_user_by_id(user_id, user_data):
    user_ref = get_user_ref(user_id)
    user_ref.update({'email': user_data.email,
                     'phone': user_data.phone,})


# def get_todos(user_id):
#     return db.collection('users')\
#         .document(user_id)\
#         .collection('todos').get()
        
# def put_todo(user_id, description):
#     todos_collection_ref = db.collection('users').document(user_id).collection('todos')
#     todos_collection_ref.add({'description': description, 'done':False})