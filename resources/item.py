from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource): #inherits from Resource
    parser = reqparse.RequestParser() #not a self variable i.e. it is common to all Item objects
    parser.add_argument('price',
            type = float,
            required = True,
            help = "this field cannot be left blank"
    )
    parser.add_argument('store_id',
            type = int,
            required = True,
            help = "Every item needs store id"
    )

    @jwt_required() #i.e. auth required for this get method
    def get(self,name): 
        item = ItemModel.find_by_name(name) 
        if item:
            return item.json()
        return {'message':'item not found'},404


#Note: code 202: accepted. Example: if post request from user is to be served later but is accepted. like if the new item will be created after a delay but is accepted for creation

    @jwt_required()
    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':'Item with name `{}` already exists'.format(name)}, 400
        data = Item.parser.parse_args()#request.get_json()  #here Item.parser as parser is not a self variable
        new_item = ItemModel(name,data['price'],data['store_id'])
        
        try:
            new_item.save_to_db()
        except:
            return {'Error message':'Error inserting item'}, 500 #internal server error

        return new_item.json(), 201 #for created

    @jwt_required()
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'} 

    @jwt_required()
    def put(self,name):
        data = Item.parser.parse_args() #will now only pass price argument to data #request.get_json()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name,data['price'],data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]} #.query.all is a sqlalchemy method to return all as objects in the table
        # or {'items':list(map(lambda x: x.json, ItemModel.query.all()))}