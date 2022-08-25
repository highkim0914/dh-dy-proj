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
    asset_name = event['pathParameters']['asset_name']
    print(asset_name)
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=get_secret(), database=DBNAME)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(f'SELECT * FROM asset where asset.name = {asset_name}')
        query_results = cur.fetchall()
        if len(query_results) == 0:
            return {
                "statusCode": 200,
                "body": "사용 가능한 asset 이름입니다."
            }
        else:
            return {
                "statusCode": 200,
                "body": "이미 존재하는 asset 이름입니다."
            }
    except Exception as e:
        print("Database connection failed due to {}".format(e))
