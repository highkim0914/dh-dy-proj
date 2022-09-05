import boto3
import pymysql
import json
import logging
import sys

ENDPOINT = "mysql.c14b7b28namw.ap-northeast-2.rds.amazonaws.com"  # rds endpoint
PORT = "3306"
USER = "admin"
REGION = "ap-northeast-2"
DBNAME = "uplus"


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId='mysqlDatabaseSecret'
    )

    database_secrets = json.loads(response['SecretString'])
    return database_secrets['password']


def get_connection():
    try:
        conn = pymysql.connect(host=ENDPOINT, user=USER, passwd=get_secret(), database=DBNAME)
        return conn
    except Exception as e:
        print("Database connection failed due to {}".format(e))
        logger.error("ERROR : Could not connect to MySQL instance")
        logger.error(e)
        sys.exit()

def get_cursor(conn):
    return conn.cursor()


def get_dict_cursor(conn):
    return conn.cursor(pymysql.cursors.DictCursor)
