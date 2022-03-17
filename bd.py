from mysql.connector import *

connection = connect(
    host="localhost",
    user="bot",
    password="bot164",
    database="bot_db")

def request(s):
    with connection.cursor() as cursor:
        cursor.execute(s)
        return cursor.fetchall()

def change(s):
    with connection.cursor() as cursor:
        cursor.execute(s)
        connection.commit()