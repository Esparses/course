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
    parse.add_argument('store_id',
            type=int,
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
        item = ItemModel(name,data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {'message': 'An error ocurred inserting the item {}'.format(item.json())},500      
        return item.json(), 201
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {'message' : 'Items was delete : "{}"'.format(name)}, 201
        else:
            return {'message' : "Item with name {} does not exists".format(name)}, 400

        
    def put(self, name):
        data = Item.parse.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 201
        
        


class ItemList(Resource):
    def get(self):    
                
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all() ))},200
