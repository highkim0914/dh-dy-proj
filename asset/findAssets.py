import datetime
import boto3
import pymysql
import json
from dbConnect import *

try:
    conn = get_connection()
except Exception as e:
    print("Database connection failed due to {}".format(e))


def get_str_value(obj):
    if isinstance(obj, datetime.datetime):
        return str(obj)
    else:
        return obj


def lambda_handler(event, context):
    query_string_dict = event['multiValueQueryStringParameters']

    where_clause_list = []
    has_where = False
    for key in query_string_dict.keys():
        if 'page' in key or 'sort' in key:
            continue
        values = query_string_dict[key]

        if '_at' in key:
            where_clause_list.append(f'{key} >= "{values[0]}" and {key} <= "{values[1]} 23:59:59" ')
            has_where = True
        else:
            if values[0] != "":
                value = '|'.join(values)
                where_clause_list.append(f'{key} regexp "{value}" ')
                has_where = True

    if has_where:
        where_clause = 'where ' + ' and '.join(where_clause_list)
    else:
        where_clause = ""

    limit = 6
    page_offset = int(event['queryStringParameters']['page_offset']) * limit
    sort = event['queryStringParameters']['sort']
    sort_by, how = sort.split(",")
    try:
        cur = get_dict_cursor(conn)
        sql_query = f'WITH filter as (' \
                    f'SELECT a.id, a.name, a.creator, a.updater, a.created_at, a.updated_at, a.asset_url, a.details, ' \
                    f'u.url ' \
                    f'FROM asset as a inner join asset_image_urls as u on a.id = u.asset_id {where_clause} ' \
                    f'group by a.id order by {sort_by} {how} ) ' \
                    f'SELECT *, (SELECT count(1) from filter) as count FROM filter ' \
                    f'limit {limit} offset {page_offset} '
        print(sql_query)
        cur.execute(sql_query)
        query_results = cur.fetchall()
        for i in range(len(query_results)):
            query_results[i] = {obj: get_str_value(query_results[i][obj]) for obj in query_results[i].keys()}
        print(query_results)
        conn.commit()
        return {
            "statusCode": 200,
            "body": json.dumps(query_results)
        }
    except Exception as e:
        print("Database connection failed due to {}".format(e))
