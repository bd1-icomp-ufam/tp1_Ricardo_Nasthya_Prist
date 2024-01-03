import re
from database_populate import populate

def extract_line(line, item_p, line_iter):
    item = item_p.copy()

    id_re = re.compile(r'Id:\s+(\d+)')
    asin_re = re.compile(r'ASIN:\s+(\S+)')
    title_re = re.compile(r'title:\s+(.*)')
    group_re = re.compile(r'group:\s+(.*)')
    salesrank_re = re.compile(r'salesrank:\s+(\d+)')
    similar_re = re.compile(r'similar:\s+(.*)')
    categories_qnt_re = re.compile(r'categories:\s+(\d+)')
    categories_re = re.compile(r'\s+\|(.+?)$')
    reviews_meta_re = re.compile(r'reviews:\s+(.*)')
    reviews_re = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})\s+cutomer:\s+(\S+)\s+rating:\s+(\d)\s+votes:\s+(\d+)\s+helpful:\s+(\d+)')

    id = id_re.search(line)
    asin = asin_re.search(line)
    title = title_re.search(line)
    group = group_re.search(line)
    salesrank = salesrank_re.search(line)
    similar = similar_re.search(line)
    categories_qnt = categories_qnt_re.search(line)
    categories = categories_re.search(line)
    reviews_meta = reviews_meta_re.search(line)
    reviews = reviews_re.search(line)

    if id:
        item['id']  = int(id.group(1))
    if asin:
        item['asin']  = asin.group(1)
    if title:
        item['title']  = title.group(1)
    if group:
        item['group']  = group.group(1)
    if salesrank:
        item['salesrank']  = int(salesrank.group(1))
    if similar:
        similar_value = similar.group(1)
        item['similar'] = similar_value.split('  ')[1:]
    if categories_qnt:
        categories_qnt_value = int(categories_qnt.group(1))

        item['categories'] = []
        for _ in range(categories_qnt_value):
            new_values = extract_line(next(line_iter), {}, line_iter)
            item['categories'].append(new_values['categories'])

    if categories:
        item['categories']  = categories.group(1)

    if reviews_meta:
        reviews_meta_value = reviews_meta.group(1)
        reviews_meta_value_parsed = dict(map(lambda x: (x.split(':')[0], float(x.split(':')[1].strip())), reviews_meta_value.split('  ')))
        item['reviews_meta'] = reviews_meta_value_parsed

        item['reviews'] = []
        for _ in range(int(reviews_meta_value_parsed['downloaded'])):
            new_values = extract_line(next(line_iter), {}, line_iter)
            if 'reviews' in new_values:
                item['reviews'].append(new_values['reviews'])
    
    if reviews:
        data = reviews.groups(0)
        item['reviews'] = {
            'date': data[0],
            'cutomer': data[1],
            'rating': int(data[2]),
            'votes': int(data[3]),
            'helpful': int(data[4]),
        }

    return item


def extract_file(file_path):
    item = {}
    
    populate_instance = populate()

    print("Inserindo dados no banco de dados...")

    with open(file_path, 'r', encoding='utf-8') as file:
        line_iter = iter(file)
        for line in line_iter:
            item = extract_line(line, item, line_iter)
            if line.strip() == '':
                populate_instance.insert(item)
                item = {}

def main(file_name):
    print(f'Extraindo dados de "{file_name}" ...')
    extract_file(file_name)
