import datetime
import boto3
import pymysql
import json
from dbConnect import *

def lambda_handler(event, context):
    asset_name = event['pathParameters']['asset_name']
    print(asset_name)
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(f'SELECT * FROM asset where asset.name = {asset_name}')
        query_results = cur.fetchall()
        conn.close()
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
