import json
from dbConnect import *

conn = get_connection()

def lambda_handler(event, context):

    # page offset, sort
    global row
    page = event['queryStringParameters']['page']

    # if input: OR절 필요
    where_or = ''
    if 'input' in event['queryStringParameters'].keys():
        input = event['queryStringParameters']['input']
        where_or = f'(m.creator like \'%{input}%\' OR' \
                   f' m.updater like \'%{input}%\' OR' \
                   f' detail like \'%{input}%\' OR' \
                   f' asset.name like \'%{input}%\')'
        if input is '': where_or = ''
    print(where_or)

    # 나머지 파라미터
    parameters = event['queryStringParameters']
    where_list = []
    for key in parameters.keys():
        if key in ('page', 'sort', 'input'): continue

        value = parameters[key]
        if value in ('null' or ''):
            continue
        print(value)
        if key[-2:] == 'id':
            where_list.append(f'{key} = {value}')
        else:
            where_list.append(f'{key} = \'{value}\'')

    where_and = 'AND ' if where_or and where_list else ''
    where_and += ' and '.join(where_list)

    isWhere = 'where' if where_or or where_and else ''

    # 쿼리 시작
    sql = f'select distinct m.id, pc.name, sc.name, detail, gender, p.name as pname, m.creator as creator, m.updater as updater, m.created_at as created_at, m.updated_at as updated_at, asset.id as asset_id' \
          f' from metadata m' \
          f' inner join primary_category as pc on primary_category_id = pc.id' \
          f' inner join secondary_category as sc on secondary_category_id = sc.id' \
          f' inner join asset on asset_id = asset.id' \
          f' inner join project as p on p.id = m.project_id' \
          f' {isWhere} {where_or} {where_and}' \
          f' order by m.updated_at DESC' \
          # f' limit 10 offset {page}'

    cursor = get_dict_cursor(conn)
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        row['created_at'] = row['created_at'].strftime("%Y/%m/%d")
        row['updated_at'] = row['updated_at'].strftime("%Y/%m/%d")

    # 커밋
    conn.commit()

    return {
        "statusCode": 200,
        "body": json.dumps(rows)
    }
