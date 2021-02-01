from database import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80)) 

    items = db.relationship('ItemModel',lazy = 'dynamic') #gets all item models with this store's id
    #'lazy = dynamic' implies that rather than creating an Item model for all items in table, it makes a query builder that looks at all item rows and can make item model objects as and when required. Saves computation

    def __init__(self,name):
        self.name = name 

    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]} #since due to lazy = dynamic, self.items is a query builder, we use .all() to retrieve all item rows as objects

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() 

    def save_to_db(self): #insert and update both
        db.session.add(self) #adds/updates the self class as row
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    