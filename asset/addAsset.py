import datetime
import boto3
import pymysql
import json
from mysqlConnect import *


def lambda_handler(event, context):
    body_json = json.loads(event['body'])
    name = body_json['name']
    asset_url = body_json['asset_url']
    image_urls = body_json['image_urls'].split(",")
    details = body_json['details']
    file_hash = body_json['file_hash']
    now = str(datetime.datetime.now())
    request_username = event['requestContext']['authorizer']['claims']['cognito:username']
    asset_value = (name, request_username, request_username, now, now, asset_url, details, file_hash)
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        insert_query = f'INSERT INTO asset ' \
                       f'(`name`, `creator`, `updater`, `created_at`, `updated_at`, `asset_url`, `details`, `file_hash`) ' \
                       f'VALUES {asset_value}'
        print(insert_query)
        cur.execute(insert_query)
        inserted_id = conn.insert_id()
        for url in image_urls:
            image_url_value = (inserted_id, url)
            insert_image_url_query = f'INSERT INTO asset_image_urls (`asset_id`, `url`) VALUES {image_url_value}'
            print(insert_image_url_query)
            cur.execute(insert_image_url_query)
        return {
            "statusCode": 200,
            "body": {
                "id": inserted_id
            }
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))
