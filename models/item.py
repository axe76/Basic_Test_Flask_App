from database import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80)) #max chars allowed = 80
    price = db.Column(db.Float(precision=2)) 

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) #id from stores table is foreign key
    store = db.relationship('StoreModel') #So now every item model has a store model that matches the store_id. 
    #db.relationship automatically finds this store using a join 

    def __init__(self,name,price,store_id):
        self.name = name #these self var names should be same as the table columns. 
        #The init method will be called for all rows, i.e. objects for all rows will be made by sqlalchemy
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #A method of SQLAlchemy model that automatically connects to database
        #and basically does the query SELECT * FROM __tablename__ WHERE name = name LIMIT 1 i.e. 1st matching element
        #then converts the resulting row into ItemModel object and returns

    def save_to_db(self): #insert and update both
        db.session.add(self) #adds/updates the self class as row
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    