from flask_login import UserMixin
from .firestore_service import get_user_by_id

class UserData:
    def __init__(self,username,password, email, phone, typeuser):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.typeuser = typeuser

class UserModel(UserMixin):
    """
    :param user_data = UserData
    """
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password
        self.email = user_data.email
        self.phone = user_data.phone
        self.typeuser = user_data.typeuser        
        
    @staticmethod
    def query(user_id):
        user_doc = get_user_by_id(user_id)
        user_data = UserData(
            username= user_doc.id,
            password = user_doc.to_dict()['password'],
            email = user_doc.to_dict()['email'],
            phone = user_doc.to_dict()['phone'],
            typeuser = 2,
        )
        
        return UserModel(user_data)