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
        if key == 'keywords': continue

        print(value)
        if key[-2:] == 'id':
            set_list.append(f'{key} = {value}')
        else:
            set_list.append(f'{key} = \'{value}\'')

    # request_username = event['requestContext']['authorizer']['claims']['cognito:username']
    request_username = "testName"  # 테스트 예시
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

    # 3. metadata_keyword 기존 삭제
    keywords = event['body']['keywords']
    # 4. metadata_keyword 생성

    # 5. 커밋
    # cursor.connection.commit()
    cursor.connection.close()
    return {
        "statusCode": 204
    }
