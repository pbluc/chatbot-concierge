import json
import boto3
from datetime import datetime

def validate(slots):
    if not slots['location']:
        return {
            'isValid': False,
            'invalidSlot': 'location'
        }
    
    if len(slots['location']['value']['resolvedValues']) == 0:
        return {
            'isValid': False,
            'invalidSlot': 'location'
        }
        
    if not slots['cuisine']:
        return {
            'isValid': False,
            'invalidSlot': 'cuisine'
        }
        
    if not slots['number_of_people']:
        return {
            'isValid': False,
            'invalidSlot': 'number_of_people'
        }
    
    if int(slots['number_of_people']['value']['resolvedValues'][0]) < 1:
        return {
            'isValid': False,
            'invalidSlot': 'number_of_people',
            'message': 'I need a party size of at least 1.'
        }
        
    if not slots['diningtime_date']:
        return {
            'isValid': False,
            'invalidSlot': 'diningtime_date'
        }
    
    now = datetime.now()
    diningtime_date = datetime.strptime(slots['diningtime_date']['value']['resolvedValues'][0], '%Y-%m-%d').date()
    if diningtime_date < now.date():
        return {
            'isValid': False,
            'invalidSlot': 'diningtime_date',
            'message': 'I need a date in the future.'
        }
    
    if not slots['diningtime_time']:
        return {
            'isValid': False,
            'invalidSlot': 'diningtime_time'
        }
    
    diningtime_time = datetime.strptime(slots['diningtime_time']['value']['resolvedValues'][0], '%H:%M').time()
    if diningtime_date == now.date() and diningtime_time < now.time():
        return {
            'isValid': False,
            'invalidSlot': 'diningtime_time',
            'message': 'I need a time in the future.'
        }
    
    if not slots['phone_number']:
        return {
            'isValid': False,
            'invalidSlot': 'phone_number'
        }
        
    phone_number = slots['phone_number']['value']['resolvedValues'][0]
    if not (len(phone_number) >= 7 and len(phone_number) <= 12):
        return {
            'isValid': False,
            'invalidSlot': 'phone_number',
            'message': 'That doesn\'t appear to be a valid phone number.'
        }
    
    return {'isValid': True}
        

def lambda_handler(event, context):
    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    
    validation_result = validate(slots)
    
    response = {}
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            if 'message' in validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": validation_result['message']
                        }
                    ]
                }
            else:
               response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        else:
            client = boto3.client("sqs")
            response = client.send_message(
                QueueUrl="https://sqs.us-east-1.amazonaws.com/205310598701/DiningConciergeQueue",
                MessageBody=json.dumps(slots))
                
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                        "state": "Fulfilled"
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": "You’re good to go! Expect my suggestions shortly! Have a great day."
                        }
                    ]
                }
            }
        
    return response