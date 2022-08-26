import json
from mysqlConnect import getDictCursor

def lambda_handler(event, context):

    # 1. 파싱
    id = event['pathParameters']['metadata_id']

    cursor = getDictCursor()
    # 2. keyword_metadata delete
    sql = f'delete from keyword_metadata where metadata_id = {id}'
    print(sql)
    cursor.execute(sql)

    # 3. metadata delete
    sql = f'delete from metadata where id = {id}'
    print(sql)
    cursor.execute(sql)

    # 4. 커밋
    # cursor.connection.commit()
    cursor.connection.close()
    return {
        "statusCode": 204
    }
