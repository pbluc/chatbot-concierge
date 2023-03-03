import json
import boto3
from datetime import datetime
client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    
    msg_from_user = event['messages'][0]['unstructured']['text']
    print(msg_from_user)
    
    response = client.recognize_text(
        botId='ZS0X7TH8GN',
        botAliasId='LBAQUJMTHK',
        localeId='en_US',
        sessionId='testuser',
        text=msg_from_user)
    
    msg_from_lex = response.get('messages', [])
    print(msg_from_lex)
    if msg_from_lex:
        resp = {
            'statusCode': 200,
            'messages': [
                {
                    'type': 'unstructured',
                    'unstructured': {
                        'text': msg_from_lex[0]['content']
                    }
                }
            ]
        }
        
        print(resp)
        return resp
