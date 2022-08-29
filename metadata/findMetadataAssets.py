import json
from mysqlConnect import getDictCursor

def lambda_handler(event, context):
    cursor = getDictCursor()
    cursor.execute('select id, name, creator, created_at from asset')
    rows = cursor.fetchall()

    for row in rows:
        row['created_at'] = row['created_at'].strftime("%Y/%m/%d/ %H:%M:%S")

    # 커밋
    # cursor.connection.commit()
    cursor.connection.close()
    return {
        "statusCode": 200,
        "body":json.dumps(rows)
    }