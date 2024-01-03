from database.setup import Db_Connection
from psycopg2 import sql

class category_repository:
    def __init__(self):
        self.db = Db_Connection().connection()
        self.cursor = self.db.cursor()

    def generate_table():
        return '''CREATE TABLE category (
            id SERIAL PRIMARY KEY,
            title VARCHAR
        );'''
    
    def drop_table():
        return '''DROP TABLE IF EXISTS category CASCADE;'''
    
    def find_category_by_name(self, name):
        query = sql.SQL('SELECT * FROM category WHERE title = {}').format(sql.Literal(name))

        self.cursor.execute(query)
        result = self.cursor.fetchone()

        return result
    
    def insert(self, title):
        query = sql.SQL('INSERT INTO category (title) VALUES ({}) RETURNING id').format(sql.Literal(title))

        self.cursor.execute(query)

        result = self.cursor.fetchone()[0]

        self.db.commit()

        return result