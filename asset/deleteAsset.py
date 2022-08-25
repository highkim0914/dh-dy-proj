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
    asset_id = event['pathParameters']['asset_id']
    print(asset_id)
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=get_secret(), database=DBNAME)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(
            f'DELETE * FROM asset inner join metadata as m on asset.id = m.asset_id where asset.id = {asset_id}')
        query_results = cur.fetchall()
        if len(query_results) == 0:
            return {
                "statusCode": 200,
                "body": "연결된 메타 데이터가 존재합니다. 삭제할 수 없습니다."
            }
        else:
            cur.execute(f'DELETE FROM asset where asset.id = {asset_id}')
            return {
                "statusCode": 200,
                "body": "asset 삭제를 성공하였습니다."
            }
    except Exception as e:
        print("Database connection failed due to {}".format(e))
