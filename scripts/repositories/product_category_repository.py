from psycopg2 import sql
from database.setup import Db_Connection

class product_category_repository:
    def __init__(self):
        self.db = Db_Connection().connection()
        self.cursor = self.db.cursor()
    
    def __del__(self):
        self.cursor.close()
        self.db.close()

    def generate_table():
        return '''CREATE TABLE product_category (
            id SERIAL PRIMARY KEY,
            product_asin VARCHAR NOT NULL,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (product_asin) REFERENCES product(asin),
            FOREIGN KEY (category_id) REFERENCES category(id)
        );'''
    
    def drop_table():
        return '''DROP TABLE IF EXISTS product_category CASCADE;'''
    
    def insert(self, product_asin, category_id):
        query = sql.SQL('INSERT INTO product_category (product_asin, category_id) VALUES ({}, {})').format(sql.Literal(product_asin), sql.Literal(category_id))

        self.cursor.execute(query)
        self.db.commit()