import json
from mysqlConnect import getDictCursor

def lambda_handler(event, context):
    cursor = getDictCursor()
    cursor.execute('select id, name, creator from asset')
    rows = cursor.fetchall()

    # 커밋
    # cursor.connection.commit()
    cursor.connection.close()
    return {
        "statusCode": 200,
        "body":json.dumps(rows)
    }