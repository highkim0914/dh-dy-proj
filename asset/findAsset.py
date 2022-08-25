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
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=get_secret(), database=DBNAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM asset")
        query_results = cur.fetchall()
        print(query_results)
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "body": json.dumps({
                "message": "hello world"
            }),
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))




