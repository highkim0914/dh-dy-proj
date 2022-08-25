import json
from mysqlConnect import getCursor

def lambda_handler(event, context):
    cursor = getCursor()
    cursor.execute("select * from primary_category")
    rows = cursor.fetchall()
    # print(rows)

    res = [dict((cursor.description[i][0], value) \
          for i, value in enumerate(row)) for row in rows]

    cursor.connection.close()
    return {
        "statusCode": 200,
        "body": json.dumps(res, ensure_ascii=False)
    }
