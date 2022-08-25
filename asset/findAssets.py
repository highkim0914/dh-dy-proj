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
    query_string_dict = event['multiValueQueryStringParameters']

    where_clause_list = []
    for key in query_string_dict.keys():
        values = query_string_dict[key]
        if len(values) == 1:
            value = str(values[0])
            print(value)
            where_clause_list.append(f'{key} = \'{value}\'')
        else:
            value = str(tuple(values))
            if 'page' in key or 'sort' in key:
                continue
            elif '_at' in key:
                where_clause_list.append(f'{key} >= {values[0]} and {key} <= {values[1]}')
            else:
                where_clause_list.append(f'{key} in {value}')

    where_clause = ' and '.join(where_clause_list)
    page_offset = event['queryStringParameters']['page_offset']
    sort = event['queryStringParameters']['sort']
    sort_by, how = sort.split(",")
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=get_secret(), database=DBNAME)
        cur = conn.cursor(pymysql.cursors.DictCursor)
        sql_query = f'SELECT * FROM asset inner join asset_image_urls as aiu on asset.id = aiu.asset_id where {where_clause} order by {sort_by} {how} limit 6 offset {page_offset}'
        print(sql_query)
        cur.execute(sql_query)
        query_results = cur.fetchall()
        for i in range(len(query_results)):
            query_results[i] = {obj: get_str_value(query_results[i][obj]) for obj in query_results[i].keys()}
        return {
            "statusCode": 200,
            "body": json.dumps(query_results)
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))