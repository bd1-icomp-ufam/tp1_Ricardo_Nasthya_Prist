from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

class Db_Connection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

    def connection(self):
        return self.conn