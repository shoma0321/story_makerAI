import json
import os
from dynamodb_handler import DynamoDBHandler
from openai_handler import OpenAIHandler
from line_handler import LineHandler

USER_TABLE_NAME = os.environ['USER_TABLE_NAME']
LOG_TABLE_NAME = os.environ['LOG_TABLE_NAME']
CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

def lambda_handler(event, context):
    body = json.loads(event['body'])

    reply_token = body['events'][0].get('replyToken', '')
    user_id = body['events'][0]['source']['userId']
    
    # Initialize handlers
    dynamodb_handler = DynamoDBHandler(USER_TABLE_NAME, LOG_TABLE_NAME)
    openai_handler = OpenAIHandler(OPENAI_API_KEY,dynamodb_handler) 
    line_handler = LineHandler(dynamodb_handler, openai_handler)

    if not body['events'][0]['type'] == 'message':
        error_message = "Error: Event is not a message type."
    elif not body['events'][0]['message']['type'] == 'text':
        error_message = "Error: Message is not a text type."
    else:
        user_message = body['events'][0]['message']['text']
        error_message = None

    user_message = body['events'][0]['message'].get('text', '')

    handle_user_message(user_message, reply_token, user_id, error_message, dynamodb_handler, openai_handler,line_handler)

    return {'statusCode': 200, 'body': json.dumps('Success!')}


def handle_user_message(user_message, reply_token, user_id, error_message, dynamodb_handler, openai_handler,line_handler):
    DEFAULT_MODE_CODE = 0
    if error_message:
        line_handler.reply_message(reply_token, error_message,DEFAULT_MODE_CODE)
        return

    # 現在のモードコードを取得します
    mode_code = dynamodb_handler.get_mode_code(user_id)

    prompt, new_mode_code, ai_response = line_handler.process_user_message(user_message, reply_token, user_id)

    if new_mode_code is not None:
        mode_code = new_mode_code
        line_handler.dynamodb_handler.update_mode_code(user_id, mode_code)  # Update the mode code in DynamoDB
    

    line_handler.dynamodb_handler.save_log(user_id, user_message, ai_response, mode_code)
    
    quick_reply_items = line_handler.generate_quick_reply_items(mode_code)
    line_handler.reply_message(reply_token, ai_response, quick_reply_items)
