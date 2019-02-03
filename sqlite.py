import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

try:
    create_table = "CREATE TABLE users (id int, username text, password text)"
    cursor.execute(create_table)
except:
    print("table already exists")

user = (1, "joel", "12345678")

insert_query = "INSERT INTO users  VALUES (?,?,?)"

cursor.execute(insert_query,user)

users =  [
    (2,"pedro","12345678"),
    (3,"julio","12345678"),
    (4,"raul","12345678"),
    (5,"alonso","12345678")
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in connection.execute(select_query):
    print(row)


connection.commit()

connection.close()