import requests
import json
import time

API_KEY = "KEY" # TODO replace with your API KEY
AAI_URL = "https://api.assemblyai.com"
transcript_url = "/v2/transcript"

HEADERS = {
    "authorization": API_KEY,
}

demo_urls = [
    "https://api.assemblyai-solutions.com/storage/v1/object/public/sam_training_bucket/Joe%20Rogan_%20Comedy,%20Controversy,%20Aliens,%20UFOs,%20Putin,%20CIA,%20and%20Freedom%20%20Lex%20Fridman%20Podcast%20?t=2023-09-05T14%3A08%3A13.934Z",
]

# The name of the file
filename = "output.txt"
transcript_id = "6m8gfeepr1-d33c-4968-a6ad-5b8ad2512230"
polling_endpoint = f"{AAI_URL}{transcript_url}/{transcript_id}"
transcription_result = requests.get(polling_endpoint, headers=HEADERS).json()
# Using the 'with' statement and 'open' function to write content to a file
with open(filename, 'w') as file:
    file.write(str(transcription_result))

print(f"content has been written to {filename}")