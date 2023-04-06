import json
import random
import boto3
import os

kinesis=boto3.client('kinesis')

adjectives = ['Electric', 'Mystical', 'Funky', 'Cosmic', 'Soulful', 'Gritty', 'Hypnotic', 'Dreamy', 'Jazzy']
nouns = ['Groove', 'Vibes', 'Harmony', 'Rhythm', 'Melody', 'Beat', 'Tune', 'Jam', 'Chord']

StreamName=os.environ['kinesistream']


def lambda_handler(event, context):
    def generate_artist_name():
            adjective = random.choice(adjectives)
            noun = random.choice(nouns)
            return f"{adjective} {noun}"
    for i in range(5):
            send= generate_artist_name()
            print(send)
            response = kinesis.put_record(
            StreamName=StreamName,
            Data=json.dumps(send),
            PartitionKey="1")







 




    


