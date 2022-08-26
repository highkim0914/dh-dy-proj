import json
from mysqlConnect import getDictCursor

def lambda_handler(event, context):

    event['body']

    cursor = getDictCursor()

    cursor.execute('select * from project')
    rows = cursor.fetchall()

    for row in rows:
        row['created_at'] = row['created_at'].strftime("%Y/%m/%d/ %H:%M:%S")
        row['updated_at'] = row['updated_at'].strftime("%Y/%m/%d/ %H:%M:%S")

    cursor.connection.close()
    return {
        "statusCode": 200,
        "body":json.dumps(rows)
    }