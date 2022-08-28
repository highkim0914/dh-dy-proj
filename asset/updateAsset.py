import datetime
import boto3
import pymysql
import json
from dbConnect import *


def lambda_handler(event, context):
    body_json = json.loads(event['body'])
    asset_id = event['pathParameters']['asset_id']
    name = body_json['name']
    asset_url = body_json['asset_url']
    image_urls = body_json['image_urls'].split(",")
    print(image_urls)
    details = body_json['details']
    file_hash = body_json['file_hash']

    now = str(datetime.datetime.now())
    username = event['requestContext']['authorizer']['claims']['cognito:username']

    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        select_query = f'SELECT * FROM asset where id = {asset_id}'
        print(select_query)
        cur.execute(select_query)
        # 기존 에셋 정보 - 이후 로그 작성 시 사용할 예정
        select_result = cur.fetchone()
        update_query = f"UPDATE asset SET `name` = '{name}'" \
                       f", `updater` = '{username}'" \
                       f", `details` = '{details}'" \
                       f", `updated_at` = '{now}'"
        if asset_url != "https://cognito-test-dy.s3.ap-northeast-2.amazonaws.com/dh/null":
            update_query = update_query + f", `asset_url` = '{asset_url}', `file_hash` = '{file_hash}'"

        update_query = update_query + f" where id = {asset_id} "
        print(update_query)
        cur.execute(update_query)

        if image_urls:
            delete_image_urls_query = f"DELETE FROM asset_image_urls where asset_id = {asset_id}"
            cur.execute(delete_image_urls_query)
            for url in image_urls:
                image_url_value = (asset_id, url)
                insert_image_url_query = f'INSERT INTO asset_image_urls (`asset_id`, `url`) VALUES {image_url_value}'
                print(insert_image_url_query)
                cur.execute(insert_image_url_query)

        conn.commit()
        return {
            "statusCode": 200,
            "body": " asset을 수정하였습니다."
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))
