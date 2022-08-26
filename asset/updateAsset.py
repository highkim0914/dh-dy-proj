import datetime
import boto3
import pymysql
import json
from mysqlConnect import *

def lambda_handler(event, context):
    body_json = json.loads(event['body'])
    id = body_json['id']
    name = body_json['name']
    asset_url = body_json['asset_url']
    image_urls = body_json['image_urls']
    details = body_json['details']
    now = str(datetime.datetime.now())
    request_username = event['requestContext']['authorizer']['claims']['cognito:username']

    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        select_query = f'SELECT * FROM asset where id = {id}'
        print(select_query)
        cur.execute(select_query)
        # 기존 에셋 정보 - 이후 로그 작성 시 사용할 예정
        select_result = cur.fetchone()
        update_query = f"UPDATE asset SET `name` = '{name}', `asset_url` = '{asset_url}', `updater` = '{request_username}, " \
                       f"`details` = '{details}', `updated_at` = '{now}' "
        print(update_query)
        cur.execute(update_query)

        delete_image_urls_query = f"DELETE FROM asset_image_urls where asset_id = {id}"
        cur.execute(delete_image_urls_query)
        for url in image_urls:
            image_url_value = (id, url)
            insert_image_url_query = f'INSERT INTO asset_image_urls (`asset_id`, `url`) VALUES {image_url_value}'
            print(insert_image_url_query)
            cur.execute(insert_image_url_query)
        return {
            "statusCode": 200,
            "body": " asset 추가가 성공하였습니다."
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))
