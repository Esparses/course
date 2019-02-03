from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 201
        else:
            return {'message': 'Store not found'}, 404
    
    def post(self, name):
        store = StoreModel.find_by_name(name)
        print(store)
        if store:
             return {'message': 'Store  already exists'}, 400
        
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An internal error'}, 500
        return store.json()

           
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
            return {'message': 'Store with name "{}" was delete'.format(name)}, 201
        
        return  {'message': 'Store with name "{}" not exists'.format(name)}, 404

class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}