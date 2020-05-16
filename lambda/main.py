import base64
import json
import os
from datetime import datetime

import boto3
import dateutil.tz


def get_data(event, ddb, table_name):
    la_time = dateutil.tz.gettz('America/Los_Angeles')
    cur_date_part = datetime.now(la_time).strftime('%Y%m%d')
    cur_time_part = datetime.now(la_time).strftime('%H%M%S')

    date_part = event['queryStringParameters']['date']
    time_start = event['queryStringParameters'].get('time_start', '000000')
    time_end = event['queryStringParameters'].get('time_end', '235959')
    disposition = 'attachment' if 'dl' in event['queryStringParameters'] else 'inline'

    if int(cur_date_part) > int(date_part) or \
            (int(cur_date_part) == int(date_part) and int(cur_time_part) > int(time_end)):
        cache_value = '86400'
    else:
        cache_value = 'no-cache'

    result = ddb.query(TableName=table_name,
                       Limit=1000,
                       ExpressionAttributeValues={':date_part': {'N': date_part},
                                                  ':time_start': {'N': time_start},
                                                  ':time_end': {'N': time_end}},
                       KeyConditionExpression='date_part = :date_part AND time_part BETWEEN :time_start AND :time_end')
    res = ''
    for response in result['Items']:
        res += response['payload']['S'] + '\n'
    return {
        'statusCode': 200,
        'body': res,
        'headers': {
            'Cache-Control': cache_value,
            'Content-Disposition': f'{disposition}; filename="{date_part}.csv"',
        }
    }


def put_data(event, ddb, table_name):
    if event['isBase64Encoded']:
        payload = base64.b64decode(event['body']).decode(encoding="utf-8")
    else:
        payload = event['body']
    time_part, date_part = payload.split(',')[:2]
    time_part = time_part.replace(':', '')
    month, day, year = date_part.split('/')
    month = month if len(month) > 1 else '0' + month
    day = day if len(day) > 1 else '0' + day
    date_part = year + month + day
    ddb.put_item(TableName=table_name,
                 Item={'date_part': {'N': date_part}, 'time_part': {'N': time_part}, 'payload': {'S': payload}})
    return {
        'statusCode': 200,
        'headers': {
            'Cache-Control': 'no-cache'
        }
    }


def handler(event, context):
    ddb = boto3.client('dynamodb')
    method = event['httpMethod']
    table_name = os.environ['WEATHERDATA_TABLE_NAME']
    if method == 'PUT':
        result = put_data(event, ddb, table_name)
    elif method == 'GET':
        result = get_data(event, ddb, table_name)
    else:
        result = {
            'statusCode': 400
        }
    return result
