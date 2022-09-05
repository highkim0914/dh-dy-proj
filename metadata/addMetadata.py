import json
import datetime
from dbConnect import *

conn = get_connection()

def lambda_handler(event, context):
    # 1. 메타 데이터 등록
    metadata = request_parsing(event)
    sql = f'INSERT INTO metadata(`asset_id`, `primary_category_id`, `secondary_category_id`, `project_id`, `gender`, `detail`, `keywords`, `updated_at`, `created_at`, `creator`, `updater`)' \
          f' VALUES {metadata}'
    print(sql)

    cursor = get_dict_cursor(conn)
    cursor.execute(sql)

    # 4. 커밋
    conn.commit()
    return {
        "statusCode": 201
    }

def request_parsing(event):
    body_json = json.loads(event['body'])

    asset_id = body_json['asset_id']
    primary_category_id = body_json['primary_category_id']
    secondary_category_id = body_json['secondary_category_id']
    gender = body_json['gender']
    project_id = body_json['project_id']
    detail = body_json['detail']
    keywords = body_json['keywords']
    now = str(datetime.datetime.now())
    request_username = event['requestContext']['authorizer']['claims']['cognito:username']
    # request_username = "testName"
    meta = (asset_id, primary_category_id, secondary_category_id,project_id, gender, detail,keywords, now, now, request_username,
            request_username)
    return meta
