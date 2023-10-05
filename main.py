import os
import boto3
import requests
from dotenv import load_dotenv
import pprint as pp
import random as rd


def create_dynamodb_table():
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv("AWS_REGION"))

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
            },
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
    return table


def download_pokemons(api_url="https://pokeapi.co/api/v2/pokemon"):
    response = requests.get(api_url)
    result = response.json()
    return result


def insert_item_to_table(details, table):
    table.put_item(
        Item={
            'name': details["name"],
            'id': details["id"],
            'weight': details["weight"],
            'height': details["height"]
        }
    )


def check_if_item_exist(details, table):
    response = table.get_item(
        Key={
            'name': details['name'],
            'id': details['id']
        }
    )
    if 'Item' in response:
        return True
    else:
        return False


def get_an_item(details, table):
    response = table.get_item(
        Key={
            'name': details['name'],
            'id': details['id']
        }
    )
    get_pokemon = response['Item']
    for (k, v) in get_pokemon.items():
        print(k, "=", v)


load_dotenv()
pokemons_table = create_dynamodb_table()
continue_drawing = True
while continue_drawing:
    draw = input("would you like to draw a pokemon?['y' or 'n'] ").lower()
    if draw == 'y':
        res = download_pokemons()
        pokemons = res["results"]
        pokemon = rd.choice(pokemons)
        pokemon_name = pokemon["name"]
        pokemon_url = pokemon["url"]
        # print(pokemon_name)
        # print(pokemon_url)
        pokemon_details = download_pokemons(pokemon_url)
        if not check_if_item_exist(pokemon_details, pokemons_table):
            insert_item_to_table(pokemon_details, pokemons_table)
        get_an_item(pokemon_details, pokemons_table)
    elif draw == 'n':
        print("no pokemon will be drawn")
        continue_drawing = False
    else:
        print("invalid input. please enter 'y' or 'n' ")
print("Goodbye!!!!")
pokemons_table.delete()
