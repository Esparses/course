from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import autenticate, identity

app = Flask(__name__)
app.secret_key = 'joel'
api = Api(app)

jwt = JWT(app, autenticate, identity)


items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x : x['name'] == name, items),None)
        return {'item' : item }, 201 if item  else 404
    
    def post(self, name ):
        if next(filter(lambda x : x['name'] == name, items),None) is not None:
            return {'message' : "An item with name {} already exists".format(name)}, 400
        data = request.get_json()
        item = {
                'name' : name , 
                'price' : data['price'
                ]}
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name , items))
        return {'message' : 'Items was delete : "{}"'.format(name)}, 201
    
    def put(self, name):
        parse = reqparse.RequestParser()
        parse.add_argument('price',
            type=float,
            required=True,
            help='This field cannot be left blank!'
        )
        data = parse.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = { 
                'name' : name,
                'price' : data['price']
            }
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items' : items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList,"/items")

app.run(debug=True)

