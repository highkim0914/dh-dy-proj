import json
from dbConnect import *

conn = get_connection()

def lambda_handler(event, context):
    cursor = get_dict_cursor(conn)
    cursor.execute("select * from primary_category")
    rows = cursor.fetchall()
    print(rows)

    # res = [dict((cursor.description[i][0], value) \
    #       for i, value in enumerate(row)) for row in rows]
    # 커밋
    conn.commit()
    return {
        "statusCode": 200,
        "body": json.dumps(rows)
    }
