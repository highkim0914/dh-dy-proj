import json
from mysqlConnect import getCursor

def lambda_handler(event, context):
    # if event['queryStringParameters']:

    if 'page' in event['queryStringParameters']: page = event['queryStringParameters']['page']
    # size = event['queryStringParameters']['page']
    # sort = event['queryStringParameters']['sort']
    primary = event['queryStringParameters']['primary']
    secondary = event['queryStringParameters']['secondary']
    # asset = event['queryStringParameters']['asset']
    # project_id = event['queryStringParameters']['project_id']
    # bar = event['queryStringParameters']['bar']

    # print(event['queryStringParameters']['page'])

    cursor = getCursor()

    sql = "select * from metadata" + \
    primary if !primary else None

    cursor.execute("")
    rows = cursor.fetchall()
    cursor.connection.close()
    return {
        "statusCode": 200,
        "body": json.dumps(rows)
    }


def dynamicQuery(condition):
