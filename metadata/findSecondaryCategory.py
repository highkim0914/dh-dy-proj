import json
from dbConnect import *

conn = get_connection()

def lambda_handler(event, context):
    cursor = get_dict_cursor(conn)
    primary_id = event['pathParameters']['primary_id']

    cursor.execute("select id, name from secondary_category where primary_category_id = %s", (primary_id))
    rows = cursor.fetchall()
    # res = [dict((cursor.description[i][0], value) \
    #       for i, value in enumerate(row)) for row in rows]

    conn.commit()
    return {
        "statusCode": 200,
        "body":json.dumps(rows)
    }

