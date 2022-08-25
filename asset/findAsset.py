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
        cur.execute(f'SELECT * FROM asset inner join asset_image_urls as aiu on asset.id = aiu.asset_id where asset.id = {asset_id}')
        query_results = cur.fetchall()
        for i in range(len(query_results)):
            query_results[i] = {obj:get_str_value(query_results[i][obj]) for obj in query_results[i].keys()}
        return {
            #"isBase64Encoded": False,
            "statusCode": 200,
            "body": json.dumps(query_results)
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))