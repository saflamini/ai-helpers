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

placeholder_urls = ["https://api.assemblyai-solutions.com/storage/v1/object/public/sam_training_bucket/hello-48300.mp3"]

transcript_ids = []
for url in demo_urls:
    body = {
      "audio_url": url,
      "auto_chapters": True,
      "speaker_labels": True,
    }
    response = requests.post(f"{AAI_URL}{transcript_url}", json=body, headers=HEADERS).json() # POST

    transcript_id = response['id']
    transcript_ids.append(transcript_id)
    polling_endpoint = f"{AAI_URL}{transcript_url}/{transcript_id}"

    while True:
      transcription_result = requests.get(polling_endpoint, headers=HEADERS).json()
      if transcription_result['status'] == 'completed':
        print(f"{transcript_id} is finished")
        break
      elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription Failed: {transcription_result['error']}")
      else:
        time.sleep(3)
print(transcript_ids)