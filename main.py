import os
import boto3
import requests
from dotenv import load_dotenv


load_dotenv()

# Get the service resource.
dynamodb = boto3.resource('dynamodb',region_name=os.getenv("AWS_REGION"))

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='Pokemons',
    KeySchema=[
        {
            'AttributeName': 'name',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'id',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'name',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'id',
            'AttributeType': 'N'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.wait_until_exists()

# Print out some data about the table.
print(table.item_count)