import sqlite3
import sys
from flask_restful import Resource, reqparse

# Path of the DB file depends from where "app.py" is executed.
db_location = "data.db"

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod        
    def find_by_username(cls, username):
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod        
    def find_by_id(cls, _id):
        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    
    # Get data from a Request
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be empty!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be empty!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "Username already Exists"}, 400

        connection = sqlite3.connect(db_location)
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User Created Successfully"}, 201
