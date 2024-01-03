from database.setup import Db_Connection
from psycopg2 import sql

class group_repository:
    def __init__(self):
        self.db = Db_Connection().connection()
        self.cursor = self.db.cursor()

    def generate_table():
        return '''CREATE TABLE "group" (
            id SERIAL PRIMARY KEY,
            title VARCHAR
        );'''
    
    def drop_table():
        return '''DROP TABLE IF EXISTS "group";'''
    
    def insert(self, title):
        query = sql.SQL('INSERT INTO "group" (title) VALUES ({}) RETURNING id').format(sql.Literal(title))

        self.cursor.execute(query)
        
        result = self.cursor.fetchone()[0]

        self.db.commit()

        return result

    def find_group_by_name(self, name):
        query = sql.SQL('SELECT * FROM "group" WHERE title = {}').format(sql.Literal(name))

        self.cursor.execute(query)
        result = self.cursor.fetchone()

        return result

