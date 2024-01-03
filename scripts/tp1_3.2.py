# script principal

import psycopg2
import sys
from database.setup import Db_Connection
from psycopg2 import OperationalError, IntegrityError
from repositories.group_repository import group_repository
from repositories.product_repository import product_repository
from repositories.category_repository import category_repository
from repositories.product_category_repository import product_category_repository
from repositories.review_repository import review_repository
from repositories.similar_repository import similar_repository
import data_extract
import dashboard

class main:
    def __init__(self):
        self.db = Db_Connection().connection()

    def generate_tables(self):
        try:
            print("Gerando Tabelas...")
            self.db.cursor().execute(
                group_repository.generate_table() + 
                product_repository.generate_table() +
                category_repository.generate_table() +
                product_category_repository.generate_table() +
                review_repository.generate_table() +
                similar_repository.generate_table()
                )

            self.db.commit()
        except OperationalError as e:
            print(f'Erro de conexão: {e}')
        except IntegrityError as e:
            print(f'Erro de integridade: {e}')
        except psycopg2.Error as e:
            print(f'Erro psycopg: {e}')
        finally:
            if self.db:
                self.db.close()
    
    def drop_tables(self):
        try:
            print("Dropando Tabelas...")
            self.db.cursor().execute(
                product_repository.drop_table() + 
                group_repository.drop_table() +
                category_repository.drop_table() +
                product_category_repository.drop_table() +
                review_repository.drop_table() +
                similar_repository.drop_table()
                )

            self.db.commit()
        except OperationalError as e:
            print(f'Erro de conexão: {e}')
        except IntegrityError as e:
            print(f'Erro de integridade: {e}')
        except psycopg2.Error as e:
            print(f'Erro psycopg: {e}')
        finally:
            if self.db:
                self.db.close()
                print("Conexão encerrada")           

    def run(self):
        if len(sys.argv) < 2:
            print("Informe o nome do arquivo a ser processado")
        else:
            file_name = sys.argv[1]
            
            main().drop_tables()
            main().generate_tables()
            data_extract.main(file_name)

main().run()