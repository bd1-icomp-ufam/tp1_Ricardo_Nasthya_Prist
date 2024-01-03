from database.setup import Db_Connection
from repositories.group_repository import group_repository
from repositories.product_repository import product_repository
from repositories.similar_repository import similar_repository
from repositories.category_repository import category_repository
from repositories.product_category_repository import product_category_repository
from repositories.review_repository import review_repository

class populate:
    def __init__(self):
        self.db = Db_Connection().connection()

    def insert(self, item):
        group_id = None
        title = ''
        asin = ''
        salesrank = 0
        avg_rating = 0.0
        
        if 'group' in item:
            try:
                group = group_repository().find_group_by_name(item['group'])

                if group:
                    group_id = group[0]

                if not group_id:
                    # Insert new group
                    group_id = group_repository().insert(item['group'])
            except Exception as e:
                print('Erro ao tratar grupo. Mais detalhes: ', e)

        if 'title' in item:
            title = item['title']

        if 'asin' in item:
            asin = item['asin']

        if 'salesrank' in item:
            salesrank = item['salesrank']

        if 'reviews_meta' in item:
            avg_rating = item['reviews_meta']['avg rating']

        if not asin:
            return

        # Insert a new product
        new_product = {
            'asin': asin,
            'title': title,
            'group_id': group_id,
            'salesrank': salesrank,
            'avg_rating': avg_rating,
        }

        product_repository().insert(new_product)

        if 'similar' in item:
            try:  
                for similar in item['similar']:
                    similar_repository().insert(asin, similar)
            except Exception as e:
                print('Erro ao tratar similar. Mais detalhes: ', e)
        
        if 'categories' in item:
            try:
                categories_id = []
                for category in item['categories']:
                    finded_category_id = None

                    finded_category = category_repository().find_category_by_name(category)

                    if finded_category:
                        finded_category_id = finded_category[0]

                    if not finded_category:
                        # Insert new category
                        finded_category_id = category_repository().insert(category)

                    if finded_category_id:
                        categories_id.append(finded_category_id)

                for category_id in categories_id:
                    product_category_repository().insert(asin, category_id)

            except Exception as e:
                print('Erro ao tratar categoria. Mais detalhes: ', e)
        
        if 'reviews' in item:
            try:
                for review in item['reviews']:
                    review_repository().insert(review, asin)
            except Exception as e:
                print('Erro ao tratar review. Mais detalhes: ', e)
                print('Item falhado: ', item)