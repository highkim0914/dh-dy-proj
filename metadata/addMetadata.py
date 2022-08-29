import json
import datetime
from mysqlConnect import getDictCursor


def lambda_handler(event, context):
    # 1. 메타 데이터 등록
    metadata = request_parsing(event)
    sql = f'INSERT INTO metadata(`asset_id`, `primary_category_id`, `secondary_category_id`, `project_id`, `gender`, `detail`, `updated_at`, `created_at`, `creator`, `updater`)' \
          f' VALUES {metadata}'
    print(sql)

    cursor = getDictCursor()
    cursor.execute(sql)
    metadata_id = cursor.connection.insert_id()
    print(id)

    # 2. keyword 있는지 확인 -> 없으면 등록
    body_json = json.loads(event['body'])
    keywords = body_json['keywords'].replace(' ', '').split(',')
    for keyword in keywords:
        if keyword in '': continue
        sql = f'select * from keyword where keyword = \'{keyword}\''
        print(sql)
        cursor.execute(sql)
        row = cursor.fetchone()

        if row is None:
            sql = f'insert into keyword(`keyword`) values  (\'{keyword}\')'
            cursor.execute(sql)
            print(sql)
            keyword_id = cursor.connection.insert_id()
        else:
            keyword_id = row['id']
        print('keyword_id : '+ str(keyword_id))

        # 3. keyword_metadata 등록
        sql = f'insert into keyword_metadata(`metadata_id`, `keyword_id`) values ({metadata_id}, {keyword_id})'
        print('keyword_metadata sql : '+ sql)
        cursor.execute(sql)

    # 4. 커밋
    cursor.connection.commit()
    cursor.connection.close()
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
    now = str(datetime.datetime.now())
    request_username = event['requestContext']['authorizer']['claims']['cognito:username']
    # request_username = "testName"
    meta = (asset_id, primary_category_id, secondary_category_id,project_id, gender, detail, now, now, request_username,
            request_username)
    return meta
