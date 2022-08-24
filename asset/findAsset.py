import boto3
import pymysql
import json

ENDPOINT="mysql.c14b7b28namw.ap-northeast-2.rds.amazonaws.com" # rds endpoint
PORT="3306"
USER="admin"
REGION="ap-northeast-2"
DBNAME="uplus"

def lambda_handler(event,context):
    client = boto3.client('rds')
    token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=token, database=DBNAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM asset")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print("Database connection failed due to {}".format(e))
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world"
        }),
    }



