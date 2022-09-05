import datetime
import boto3
import pymysql
import json
from dbConnect import *

try:
    conn = get_connection()
except Exception as e:
    print("Database connection failed due to {}".format(e))


def lambda_handler(event, context):
    asset_id = event['pathParameters']['asset_id']
    print(asset_id)
    try:
        cur = get_dict_cursor(conn)
        cur.execute(
            f'SELECT * FROM metadata as m where m.asset_id = {asset_id}')
        query_results = cur.fetchall()
        print(query_results)
        if query_results:
            conn.commit()
            return {
                "statusCode": 200,
                "body": "failed"
            }
        else:
            cur.execute(f'DELETE FROM asset_image_urls as u where u.asset_id = {asset_id}')
            cur.execute(f'DELETE FROM asset where asset.id = {asset_id}')
            conn.commit()
            return {
                "statusCode": 200,
                "body": "success"
            }
    except Exception as e:
        print("Database connection failed due to {}".format(e))
