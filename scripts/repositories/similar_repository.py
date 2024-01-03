from psycopg2 import sql
from database.setup import Db_Connection

class similar_repository:
    def __init__(self):
        self.db = Db_Connection().connection()
        self.cursor = self.db.cursor()
    
    def __del__(self):
        self.cursor.close()
        self.db.close()

    def generate_table():
        return '''CREATE TABLE "similar" (
            id SERIAL PRIMARY KEY,
            product1_asin VARCHAR NOT NULL,
            product2_asin VARCHAR NOT NULL,
            FOREIGN KEY (product1_asin) REFERENCES product(asin)
        );'''
    
    def drop_table():
        return '''DROP TABLE IF EXISTS "similar" CASCADE;'''
    
    def insert(self, similar_1, similar_2):
        query = sql.SQL('INSERT INTO "similar" (product1_asin, product2_asin) VALUES ({}, {})').format(sql.Literal(similar_1), sql.Literal(similar_2))

        self.cursor.execute(query)
        self.db.commit()
        