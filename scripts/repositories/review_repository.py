from database.setup import Db_Connection
from psycopg2 import sql

class review_repository:
    def __init__(self):
        self.db = Db_Connection().connection()
        self.cursor = self.db.cursor()

    def generate_table():
        return '''CREATE TABLE review (
            id SERIAL PRIMARY KEY,
            product_asin VARCHAR NOT NULL,
            created_date DATE NOT NULL,
            cutomer VARCHAR,
            rating INTEGER,
            votes INTEGER,
            helpful INTEGER,
            FOREIGN KEY (product_asin) REFERENCES product(asin)
        );'''
    
    def drop_table():
        return '''DROP TABLE IF EXISTS review CASCADE;'''
    
    def insert(self, review, product_asin):
        query = sql.SQL('INSERT INTO review (product_asin, created_date, cutomer, rating, votes, helpful) VALUES ({}, {}, {}, {}, {}, {})').format(
            sql.Literal(product_asin),
            sql.Literal(review['date']),
            sql.Literal(review['cutomer']),
            sql.Literal(review['rating']),
            sql.Literal(review['votes']),
            sql.Literal(review['helpful'])
        )

        self.cursor.execute(query)
        self.db.commit()