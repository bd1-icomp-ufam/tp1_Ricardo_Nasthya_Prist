# script para as consultas do dashboard
from database.setup import Db_Connection
from psycopg2 import sql

class dashboard:
    def __init__(self):
        self.db = Db_Connection().connection()
        self.cursor = self.db.cursor()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def consulta_a(self, asin):
        print("# Consulta A)")
        query1 = sql.SQL('SELECT * FROM review WHERE product_asin = {} order by helpful desc, rating  desc limit 5').format(sql.Literal(asin))
        query2 = sql.SQL('SELECT * FROM review WHERE product_asin = {} order by helpful desc, rating  asc limit 5').format(sql.Literal(asin))

        self.cursor.execute(query1)
        result1 = self.cursor.fetchall()

        print("\t- 5 comentários mais úteis e com maior avaliação:")

        for row in result1:
            print("\t\t- Cliente: " + row[3] + " - Avaliação: " + str(row[4]) + " - Votos: " + str(row[5]) + " - Útil: " + str(row[6]))

        self.cursor.execute(query2)
        result2 = self.cursor.fetchall()

        print("\t- 5 comentários mais úteis e com menor avaliação:")
        for row in result2:
            print("\t\t- Cliente: " + row[3] + " - Avaliação: " + str(row[4]) + " - Votos: " + str(row[5]) + " - Útil: " + str(row[6]))

    def consulta_b(self, asin):
        print("# Consulta B")
        
        query = sql.SQL('''SELECT p_similar.asin AS similar_asin,
                p_similar.title AS similar_title,
                p_similar.salesrank AS similar_salesrank
            FROM product AS p
            JOIN "similar" ON p.asin = "similar".product1_asin
            JOIN product AS p_similar ON "similar".product2_asin = p_similar.asin
            WHERE p.asin = {}
                AND p.salesrank < p_similar.salesrank
            ORDER BY p_similar.salesrank ASC
            LIMIT 5''').format(sql.Literal(asin))

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        print("\t- Produtos similares com maiores vendas:")
        for row in result:
            print("\t\t- ASIN: " + str(row[0]) + " - Título: " + row[1] + " - Vendas Rank: " + str(row[2]))
    
    def consulta_c(self, asin):
        print("# Consulta C")
        
        query = sql.SQL("""
             SELECT created_date, avg(avg(rating)) over (order by created_date) as daily_avg
            FROM review
            WHERE product_asin = {}
            group by created_date
            order by created_date
        """).format(sql.Literal(asin))

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        print("\t- Evolução diária das médias de avaliação:")
        for row in result:
            print("\t\t- Data: " + str(row[0]) + " - Média de Avaliação: " + str(row[1]))

    def consulta_d(self):
        print("# Consulta D")

        query_groups = sql.SQL('''
            SELECT id FROM "group"
        ''')
        self.cursor.execute(query_groups)
        groups = self.cursor.fetchall()

        print("\t- Top 10 produtos líderes de venda por grupo:")
        
        for group in groups:
            group_id = group[0]
            print("\t\t# Grupo ID: " + str(group_id))

            query_products = sql.SQL('''
            select * from product p where group_id = {} order by salesrank desc limit 10
            ''').format(sql.Literal(group_id))
            self.cursor.execute(query_products)
            products = self.cursor.fetchall()

            for product in products:
                print("\t\t\t- ASIN: " + str(product[0]) + " - Título: " + product[1] + " - Vendas Rank: " + str(product[3]))

    def consulta_e(self):
        print("# Consulta E")

        query = """
            SELECT
                p.asin,
                p.title,
                AVG(r.helpful) AS media_uteis_positivas
            FROM product p
            JOIN review r ON p.asin = r.product_asin
            WHERE r.helpful > 0
            GROUP BY p.asin, p.title
            ORDER BY media_uteis_positivas DESC
            LIMIT 10;
        """

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        print("\t- Top 10 produtos com maior média de avaliações úteis positivas:")
        for row in result:
            print("\t\t- ASIN: " + str(row[0]) + " - Título: " + row[1] + " - Média de Avaliações Úteis Positivas: " + str(row[2]))

    def consulta_f(self):
        print("# Consulta F")

        query = sql.SQL("""
            select c.title AS categoria, AVG(r.helpful) AS media_uteis_positivas
            from product_category pc 
            join category c on c.id = pc.category_id
            join review r on r.product_asin = pc.product_asin
            where r.helpful > 0
            group by c.id
            order by media_uteis_positivas desc
            limit 5
        """)

        self.cursor.execute(query)
        result = self.cursor.fetchall()

        print("\t- Top 5 categorias com maior média de avaliações úteis positivas:")
        for row in result:
            print("\t\t- Categoria: " + row[0] + " - Média de Avaliações Úteis Positivas: " + str(row[1]))

    def consulta_g(self):
        print("# Consulta G")

        query_groups = sql.SQL('''
            SELECT id FROM "group"
        ''')
        self.cursor.execute(query_groups)
        groups = self.cursor.fetchall()

        print("\t- Top 10 clientes que mais fizeram comentários por grupo de produto:")
        for group in groups:
            group_id = group[0]
            print("\t\t# Grupo ID: " + str(group_id))

            query_cutomer = sql.SQL('''
            select cutomer, count(*) as total from review r
            join product p on p.asin = r.product_asin
            where group_id = {}
            group by cutomer
            order by total desc
            limit 10''').format(sql.Literal(group_id))
            self.cursor.execute(query_cutomer)
            cutomers = self.cursor.fetchall()

            for cutomer in cutomers:
                print("\t\t\t- Cliente: " + cutomer[0] + " - Total de Comentários: " + str(cutomer[1]))

    def show(self):
        print("\tConsultas do Dashboard\t")

        self.consulta_a('0790747324')
        self.consulta_b('0827229534')
        self.consulta_c('0790747324')
        self.consulta_d()
        self.consulta_e()
        self.consulta_f()
        self.consulta_g()      
        pass