import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

db_location = "data.db"

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left empty!"
    )

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            response = {"item": {
                'name': row[0],
                'price': row[1]
            }}
            return response, 200
    
        response = {
            "message": "Item Not Found"
        }
        return response, 400

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