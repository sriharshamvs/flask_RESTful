from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from helpers.security import authenticate, identity
from helpers.user import UserRegister

app = Flask(__name__)
app.secret_key = "mvs"
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left empty!"
    )

    @jwt_required()
    def get(self, name):
        # "next" gives the first item found by the filter function
        # if the "next" doesn't find anything it will retrun None
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
 
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda  x: x['name'] != name, items))
        return {'message': 'Item Deleted'}

    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        
        data = Item.parser.parse_args()

        if item is None:
            item = {
                'name': name,
                'price': data['price']
            }
            items.append(item)
        else:
            item.update(data)
        
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)