import json
import datetime
from dbConnect import *

conn = get_connection()
def lambda_handler(event, context):

    # 1. body parsing
    id = event['pathParameters']['metadata_id']

    parameters = json.loads(event['body'])
    set_list = []
    for key in parameters.keys():
        value = parameters[key]

        print(value)
        if key[-2:] == 'id':
            set_list.append(f'{key} = {value}')
        else:
            if value in ('null' or ''):
                continue
            set_list.append(f'{key} = \'{value}\'')

    request_username = event['requestContext']['authorizer']['claims']['cognito:username']
    set_list.append(f'updater = \'{request_username}\'')
    now = str(datetime.datetime.now())
    set_list.append(f'updated_at = \'{now}\'')

    set = 'set '
    set += ', '.join(set_list)

    # 2. alter sql
    sql = f'UPDATE metadata {set} WHERE id = {id}'
    print(set)
    cursor = get_dict_cursor(conn)
    cursor.execute(sql)
    a=1
    # 5. 커밋
    conn.commit()
    return {
        "statusCode": 204
    }
