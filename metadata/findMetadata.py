import json
from mysqlConnect import getDictCursor

def lambda_handler(event, context):

    # 1. body parsing
    id = event['pathParameters']['metadata_id']

    # 2. meatadata 검색 , keyword 처리
    sql = f'select * from metadata as m' \
          f' inner join keyword_metadata as km on m.id = km.metadata_id' \
          f' inner join keyword as k on km.keyword_id = k.id' \
          f' where m.id = {id}'
    print(sql)
    cursor = getDictCursor()
    cursor.execute(sql)
    rows = cursor.fetchall()

    # 커밋
    # cursor.connection.commit()
    cursor.connection.close()

    for row in rows:
        row['created_at'] = row['created_at'].strftime("%Y/%m/%d/ %H:%M:%S")
        row['updated_at'] = row['updated_at'].strftime("%Y/%m/%d/ %H:%M:%S")

    return {
        "statusCode": 200,
        "body": json.dumps(rows)
    }
