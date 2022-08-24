import json

def lambda_handler(event, context):
    return json.dumps(event);