import json
from dbConnect import *

conn = get_connection()

def lambda_handler(event, context):
    cursor = get_dict_cursor(conn)
    cursor.execute('select id, name, creator, created_at from asset')
    rows = cursor.fetchall()

    for row in rows:
        row['created_at'] = row['created_at'].strftime("%Y/%m/%d/ %H:%M:%S")

    # 커밋
    conn.commit()
    return {
        "statusCode": 200,
        "body":json.dumps(rows)
    }