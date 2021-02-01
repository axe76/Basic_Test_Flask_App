import sqlite3
from database import db

#models are the helper classes that help the backend code. Like in security.py

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80)) #max chars allowed = 80
    password = db.Column(db.String(80)) 

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self) #adds/updates the self class as row
        db.session.commit()
    
    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id =_id).first()