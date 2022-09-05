import json
from dbConnect import *

conn = get_connection()

def lambda_handler(event, context):

    # 1. body parsing
    id = event['pathParameters']['metadata_id']

    # 2. meatadata 검색 , keyword 처리
    sql = f'select * from metadata as m' \
          f' inner join primary_category as pc on primary_category_id = pc.id' \
          f' inner join secondary_category as sc on secondary_category_id = sc.id' \
          f' where m.id = {id}'
    print(sql)
    cursor = get_dict_cursor(conn)
    cursor.execute(sql)
    rows = cursor.fetchall()

    # 커밋
    conn.commit()

    for row in rows:
        row['created_at'] = row['created_at'].strftime("%Y/%m/%d/ %H:%M:%S")
        row['updated_at'] = row['updated_at'].strftime("%Y/%m/%d/ %H:%M:%S")

    return {
        "statusCode": 200,
        "body": json.dumps(rows)
    }
