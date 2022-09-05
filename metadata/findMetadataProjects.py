import json
from dbConnect import *

conn = get_connection()

def lambda_handler(event, context):
    cursor = get_dict_cursor(conn)


    cursor.execute('select * from project')
    rows = cursor.fetchall()

    for row in rows:
        row['created_at'] = row['created_at'].strftime("%Y/%m/%d/ %H:%M:%S")
        row['updated_at'] = row['updated_at'].strftime("%Y/%m/%d/ %H:%M:%S")

    # 커밋
    conn.commit()
    return {
        "statusCode": 200,
        "body":json.dumps(rows)
    }