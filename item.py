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

    # DB operation Methods
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return row

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
    
    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close() 

    # CRUD Operations 
    
    #Create
    @jwt_required()
    def post(self, name):
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        try:
            Item.insert_item(item)
        except:
            return {"message": "Error Occured inserting Item"}, 500
        
        return item, 201
    
    # Read
    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            response = {"item": {
                'name': item[0],
                'price': item[1]
            }}
            return response, 200
        
        response = {
            "message": "Item Not Found"
        }
        return response, 400

    # Update
    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {
                'name': name,
                'price': data['price']
            }
        if item is None:
            try:
                Item.insert_item(updated_item)
            except:
                return {"message": "Error Occured inserting Item"}, 500
        else:
            try:
                Item.update_item(updated_item)
            except:
                return {"message": "Error Occured Updating Item"}, 500
        
        return updated_item, 201

    # Delete
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()       

        return {'message': 'Item Deleted'}, 201

class ItemList(Resource):
    # Read all the Items 
    def get(self):
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        
        items = []
        for row in result:
            items.append({
                'name': row[0],
                'price': row[1]
            })

        connection.commit()
        connection.close()

        return {'items': items}, 200