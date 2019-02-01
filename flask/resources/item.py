import sqlite3
from flask_restful import Resource, reqparse
from models.item import ItemModel
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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 201
        return{'message' : 'Item not found'}, 404
    
    def post(self, name ):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name {} already exists".format(name)}, 400
        data = Item.parse.parse_args()
        item = ItemModel(name,data['price'])
        
        try:
            item.insert()
        except:
            return {'message': 'An error ocurred inserting the item {}'.format(item.json())},500
        
        return item.json(), 201
    
    def delete(self, name):
        if not(ItemModel.find_by_name(name)):
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
        item = ItemModel(name, data['price'])
        if ItemModel.find_by_name(name):
            item.update()
        else:
            item.insert()
        
        return item.json(), 201
        
        


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
