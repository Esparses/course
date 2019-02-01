import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
class Item(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('price',
            type=float,
            required=True,
            help='This field cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):     
        item = self.find_by_name(name)
        if item:
            return item, 201
        return{'message' : 'Item not found'}, 404
    
    def post(self, name ):
        if self.find_by_name(name):
            return {'message' : "An item with name {} already exists".format(name)}, 400
        data = Item.parse.parse_args()
        item = {
                'name' : name , 
                'price' : data['price'
                ]}
        try:
            self.insert(item)
        except:
            return {'message': 'An error ocurred inserting the item {}'.format(item)},500
        
        return item, 201
    
    def delete(self, name):
        if not(self.find_by_name(name)):
            return {'message' : "Item with name {} does not exists".format(name)}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
        return {'message' : 'Items was delete : "{}"'.format(name)}, 201
    
    def put(self, name):
        data = Item.parse.parse_args()
        item = {'name': name, 'price': data['price']}
        if self.find_by_name(name):
            self.update(item)
        else:
            self.insert(item)
        
        return item, 201
        
        
    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item' : {'name' : row[0], 'price':row[1]} }
        else:
            return None

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item['name'], item['price']))
        connection.commit()
        connection.close() 
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE  items set price=? WHERE name=?"
        cursor.execute(query,(item['price'], item['name']))
        connection.commit()
        connection.close() 

class ItemList(Resource):
    def get(self):    
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            item = {'name': row[0], 'price':row[1]}
            items.append(item)
        
        return {'items': items},200
