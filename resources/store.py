from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource): 
    
    def get(self,name): 
        store = StoreModel.find_by_name(name) 
        if store:
            return store.json()
        return {'message':'Store not found'},404

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message':'Store with name `{}` already exists'.format(name)}, 400
        
        new_store = StoreModel(name)
        
        try:
            new_store.save_to_db()
        except:
            return {'Error message':'Error creating store'}, 500 #internal server error

        return new_store.json(), 201 #for created

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message':'Store deleted'} 


class StoreList(Resource):
    def get(self):
        return {'Stores':[store.json() for store in StoreModel.query.all()]} 