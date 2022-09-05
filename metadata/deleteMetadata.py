import json
from dbConnect import *

conn = get_connection()

def lambda_handler(event, context):

    # 1. 파싱
    id = event['pathParameters']['metadata_id']

    cursor = get_dict_cursor(conn)

    # 2. metadata delete
    sql = f'delete from metadata where id = {id}'
    print(sql)
    cursor.execute(sql)

    # 3. 커밋
    conn.commit()
    return {
        "statusCode": 204
    }
