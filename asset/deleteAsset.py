import datetime
import boto3
import pymysql
import json
from dbConnect import *

def lambda_handler(event, context):
    asset_id = event['pathParameters']['asset_id']
    print(asset_id)
    try:
        conn = get_connection()
        cur = get_dict_cursor(conn)
        cur.execute(
            f'SELECT * FROM asset inner join metadata as m on asset.id = m.asset_id where asset.id = {asset_id}')
        query_results = cur.fetchall()
        if len(query_results) == 0:
            return {
                "statusCode": 200,
                "body": "연결된 메타 데이터가 존재합니다. 삭제할 수 없습니다."
            }
        else:
            cur.execute(f'DELETE FROM asset where asset.id = {asset_id}')
            conn.commit()
            return {
                "statusCode": 200,
                "body": "asset 삭제를 성공하였습니다."
            }
    except Exception as e:
        print("Database connection failed due to {}".format(e))
