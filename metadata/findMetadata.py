import json
from mysqlConnect import getCursor
from mysqlConnect import getDictCursor

def lambda_handler(event, context):

    page = event['queryStringParameters']['page']

    parameters = event['queryStringParameters']
    where_list = []
    for key in parameters.keys():
        value = parameters[key]
        if key in ('page', 'sort', 'size'): continue

        print(value)
        if key[-2:] == 'id':
            where_list.append(f'{key} = {value}')
        else:
            where_list.append(f'{key} = \'{value}\'')

    cursor = getDictCursor()

    where = 'where ' if len(where_list) != 0 else ''
    where += ' and '.join(where_list)
    sql = f'select * from metadata' \
          f' inner join primary_category as pc on primary_category_id = pc.id' \
          f' inner join secondary_category as sc on secondary_category_id = sc.id' \
          f' left join project on project_id = project.id' \
          f' left join keyword_metadata as km on keyword_metadata_id = km.metadata_id' \
          f' left join keyword on km.keyword_id = keyword.keyword' \
          # f' where keyword.keyword like \'%key%\')'
          # f' {where} limit 10 offset {page}'

    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    cursor.connection.close()
    for row in rows:
        row['created_at'] = row['created_at'].strftime("%Y/%m/%d/ %H:%M:%S")
        row['updated_at'] = row['updated_at'].strftime("%Y/%m/%d/ %H:%M:%S")

    return {
        "statusCode": 200,
        "body": json.dumps(rows)
    }
