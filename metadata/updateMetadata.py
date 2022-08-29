import json
import datetime
from mysqlConnect import getDictCursor

def lambda_handler(event, context):

    # 1. body parsing
    id = event['pathParameters']['metadata_id']

    parameters = event['body']
    set_list = []
    for key in parameters.keys():
        value = parameters[key]

        print(value)
        if key[-2:] == 'id':
            set_list.append(f'{key} = {value}')
        else:
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
    cursor = getDictCursor()
    cursor.execute(sql)


    # 5. 커밋
    # cursor.connection.commit()
    cursor.connection.close()
    return {
        "statusCode": 204
    }
