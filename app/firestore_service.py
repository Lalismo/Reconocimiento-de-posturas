import os
from google.cloud import firestore
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
project_id = 'tesis-405201'

firebase_admin.initialize_app(credential, {
    'projectId': project_id,
})

# Now initialize the Firestore client
db = firestore.client()

def get_type(user_id):
    # Referencia al documento del usuario
    user_ref = db.collection('users').document(user_id)

    # Obtiene los datos del documento
    user_data = user_ref.get()

    # Verifica si el documento existe
    if user_data.exists:
        # Accede al campo 'type' del documento
        user_type = user_data.get('typeuser')
        return user_type
    else:
        # Si el documento no existe, puedes manejarlo de acuerdo a tus necesidades
        print(f'El usuario con ID {user_id} no existe.')
        return None

def get_users():
    return db.collection('users').get()

def get_user_by_id(user_id):
    return db.collection('users').document(user_id).get()

def user_put_data(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({ 'password':user_data.password,
                  'email':user_data.email,
                  'typeuser': user_data.typeuser,})

def delete_user_by_id(user_id):
    user_ref = get_user_ref(user_id)
    user_ref.delete()
   
  
   
def get_user_ref(user_id):
    return db.collection('users').document(user_id)    

def update_user_by_id(user_id, email):
    user_ref = _get_user_ref(user_id)
    user_ref.update(
        {'email': email,}
    )

def _get_user_ref(user_id):
    return db.document(f'users/{user_id}')
