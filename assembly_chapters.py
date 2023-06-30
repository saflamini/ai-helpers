import requests
import json
import time
import os

assembly_url = "https://api.assemblyai.com/v2"
assembly_key = os.environ.get("ASSEMBLYAI_KEY")

headers = {
    "authorization": assembly_key,
}

#this is a local file - replace with your own
with open("./DDS_Alluo_Audio.mp3", "rb") as f:
    response = requests.post(assembly_url + "/upload",
                             headers=headers,
                             data=f)
print(response.json())
upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url,
    "auto_chapters": True,
    "word_boost": ['DeFi', 'Alluo', 'Devs Do Something', 'Superfluid', 'ibAlluo', 'stIbAlluo', 'Remy', 'Sung'], #note that this should make our transcription more likely to get these words correct
    "boost_param": 'high',
    "custom_spelling": [
        {
            'from': 'alluo',
            'to': 'Alluo'
        },
        {
            'from': 'Aluo',
            'to': 'Alluo'
        },
        {
            'from': 'Blockchain',
            'to': 'blockchain'
        },
        {
            'from': 'ib Alluo',
            'to': 'ibAlluo'
        },
        {
            'from': 'D Five',
            'to': 'DeFi'
        }
    ],
    "speaker_labels": True,
    "sentiment_analysis": True,
}

url = assembly_url + "/transcript"
response = requests.post(url, json=data, headers=headers)

print(response.json())

transcript_id = response.json()["id"]

polling_endpoint = f"{assembly_url}/transcript/{transcript_id}"

# existing_transcript_id = '6z1ruxq03q-fa4d-49c5-beaa-cf5b6a9b4efa'

# existing_endpoint = f"{assembly_url}/transcript/{existing_transcript_id}"

# existing_transcript_result = requests.get(existing_endpoint, headers=headers).json()

# print(existing_transcript_result['chapters'])


while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()

    if transcription_result['status'] == 'completed':
        chapters = transcription_result['chapters']
        print(chapters)

        # Iterate through each chapter and print data for it
        print('chapter with gist')
        for chapter in chapters:
            print(f"{chapter['start']}: {chapter['gist']}")
        
        print('chapter with headline')
        for chapter in chapters:
            print(f"{chapter['start']}: {chapter['headline']}")

        print('chapter with summary')
        for chapter in chapters:
            print(f"{chapter['start']}: {chapter['summary']}")
        break
    
    elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
    
    else: 
        time.sleep(3)