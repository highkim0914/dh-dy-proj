import datetime
import boto3
import pymysql
import json
from mysqlConnect import *

def lambda_handler(event, context):
    asset_id = event['pathParameters']['asset_id']
    print(asset_id)
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(f'SELECT * FROM asset inner join asset_image_urls as aiu on asset.id = aiu.asset_id where asset.id = {asset_id}')
        query_results = cur.fetchall()
        for i in range(len(query_results)):
            query_results[i] = {obj:get_str_value(query_results[i][obj]) for obj in query_results[i].keys()}
        return {
            "statusCode": 200,
            "body": json.dumps(query_results)
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))

