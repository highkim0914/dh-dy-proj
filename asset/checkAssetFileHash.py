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


def lambda_handler(event, context):
    asset_id = event['pathParameters']['asset_id']
    uploading_hash = event['queryStringParameters']['hash']
    print(asset_id)
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=get_secret(), database=DBNAME)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(f'SELECT asset.asset_hash FROM asset where asset.id = {asset_id}')
        query_results = cur.fetchall()
        existing_hash = query_results[0]['asset_hash']
        if uploading_hash == existing_hash:
            return {
                "statusCode": 200,
                "body": "같은 파일입니다."
            }
        else:
            return {
                "statusCode": 200,
                "body": "다른 파일입니다."
            }

    except Exception as e:
        print("Database connection failed due to {}".format(e))
