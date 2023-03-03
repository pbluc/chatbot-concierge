import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from datetime import datetime
import os

client = boto3.client('s3')
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    bucket_name = 'dining.chatbot.concierge.com'
    bucket = s3.Bucket(bucket_name)
    
    cuisineTypes =  ["Italian"] # ["Chinese", "Greek", "Italian", "Mexican", "Indian", "Thai"]
    
    
    index_id = (10*10*17)
    for cuisine in cuisineTypes:
        for i in range(20):
            filename = "restaurants/{}/{}.json".format(cuisine.lower(), i)
            
            response = client.get_object(Bucket=bucket_name, Key=filename)
            file_contents = response["Body"].read().decode('utf')
            json_contents = json.loads(file_contents)
            
            businesses = json_contents['businesses']
            
            #insert_data(businesses)
            for business in businesses:
                key = {
                    "businessID": business['id']
                }
                data = lookup_data(key)
                if len(data) != 0:
                    index = {
                        "index": {
                            "_index": "restaurants", 
                            "_id": index_id + 1
                        }
                    }
                    entry = {
                        "RestaurantID": business['id'],
                        "Cuisine": cuisine
                    }
                    print(json.dumps(index))
                    print(json.dumps(entry))
                    '''
                    with open('/restaurants.json', 'a') as f:
                        json.dump(index.json(), f)
                        json.dump(entry.json(), f)
                    '''
                    
                    index_id = index_id + 1
    
    return 

def insert_data(data_list, db=None, table='yelp-restaurants'):
    response = 0
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    # overwrite if the same index is provided
    for data in data_list:
        business = {
            'businessID': data['id'],
            'name': data['name'],
            'address': data['location']['address1'],
            'coordinates': data['coordinates'],
            'number_of_reviews': data['review_count'],
            'rating': data['rating'],
            'zip_code': data['location']['zip_code'],
            'insertedAtTimestamp': datetime.now()
        }
        business = json.loads(json.dumps(business, default=str), parse_float=Decimal)
        #print(business)
        response = table.put_item(Item=business)
    #print('@insert_data: response', response)
    return response

def lookup_data(key, db=None, table='yelp-restaurants'):
    response = {}
    if not db:
        db = boto3.resource('dynamodb')
    table = db.Table(table)
    try:
        response = table.get_item(Key=key)
    except ClientError as e:
        print('Error', e.response['Error']['Message'])
    else:
        if 'Item' in response:
            return response['Item']
        else:
            return {}
