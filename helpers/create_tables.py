import sqlite3

db_location = "data.db"

connection = sqlite3.connect(db_location)
cursor = connection.cursor()

# For auto increment we use INTEGER PRIMARY KEY
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()
connection.close()