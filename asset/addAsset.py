import datetime
import boto3
import pymysql
import json

ENDPOINT = "mysql.c14b7b28namw.ap-northeast-2.rds.amazonaws.com"  # rds endpoint
PORT = "3306"
USER = "admin"
REGION = "ap-northeast-2"
DBNAME = "uplus"


def get_secret():
    client = boto3.client('secretsmanager')

    response = client.get_secret_value(
        SecretId='mysqlDatabaseSecret'
    )

    database_secrets = json.loads(response['SecretString'])
    return database_secrets['password']


def get_str_value(obj):
    if isinstance(obj, datetime.datetime):
        return str(obj)
    else:
        return obj


def lambda_handler(event, context):
    body_json = json.loads(event['body'])
    name = body_json['name']
    asset_url = body_json['asset_url']
    image_urls = body_json['image_urls']
    details = body_json['details']
    creator = body_json['creator']
    now = str(datetime.datetime.now())
    asset_value = (name, creator, creator, now, now, asset_url)
    print(asset_value)
    request_username = event['requestContext']['authorizer']['claims']['cognito:username']
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=get_secret(), database=DBNAME)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        insert_query = f'INSERT INTO asset (`name`, `creator`, `updater`, `created_at`, `updated_at`, `asset_url`) VALUES {asset_value}'
        print(insert_query)
        cur.execute(insert_query);
        inserted_id = conn.insert_id()
        for url in image_urls:
            image_url_value = (inserted_id, url)
            insert_image_url_query = f'INSERT INTO asset_image_urls (`asset_id`, `url`) VALUES {image_url_value}'
            print(insert_image_url_query)
            cur.execute(insert_image_url_query)
        return {
            "statusCode": 200,
            "body": " asset 추가가 성공하였습니다."
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))