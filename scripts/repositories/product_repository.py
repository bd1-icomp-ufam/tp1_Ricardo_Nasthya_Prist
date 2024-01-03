from database.setup import Db_Connection
from psycopg2 import sql

class product_repository:
    def __init__(self):
        self.db = Db_Connection().connection()
        self.cursor = self.db.cursor()

    def generate_table():
        return '''CREATE TABLE product (
            asin VARCHAR PRIMARY KEY,
            title VARCHAR,
            group_id INTEGER,
            salesrank INTEGER,
            avg_rating FLOAT,
            FOREIGN KEY (group_id) REFERENCES "group"(id) ON DELETE CASCADE
        );'''
    
    def drop_table():
        return '''DROP TABLE IF EXISTS product CASCADE;'''
    
    def insert(self, product):
        query = '''
            INSERT INTO product 
            (asin, title, salesrank, avg_rating, group_id)
            VALUES (%s, %s, %s, %s, %s)'''

        self.cursor.execute(query, (product['asin'], product['title'], product['salesrank'], product['avg_rating'], product['group_id']))
        self.db.commit()