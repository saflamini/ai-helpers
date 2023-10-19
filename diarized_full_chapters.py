from output import json_output

#Give this function a json response that has auto_chapters and speaker_labels set to true
#see the output formatted in a way that makes it easy to embed & store each individual chapter in a vector DB
def speaker_diarized_output(json_response):
    # Check if auto_chapters and speaker_labels are true
    if not (json_response.get('auto_chapters') and json_response.get('speaker_labels')):
        return None

    chapters = json_response.get('chapters', [])
    utterances = json_response.get('utterances', [])

    diarized_output = []

    for chapter in chapters:
        chapter_start = chapter['start']
        chapter_end = chapter['end']

        # Filter utterances that fall within the chapter's start and end time
        relevant_utterances = [u for u in utterances if u['start'] >= chapter_start and u['end'] <= chapter_end]

        # Generate the speaker diarized output for each relevant utterance
        chapter_transcript = []
        for utterance in relevant_utterances:
            speaker = utterance['speaker']
            start_time = utterance['start']
            end_time = utterance['end']
            text = utterance['text']

            formatted_output = f"Speaker {speaker} [{start_time/1000:.2f} - {end_time/1000:.2f}]: {text}"
            chapter_transcript.append(formatted_output)

        diarized_output.append({
            'chapter_summary': chapter['summary'],
            'transcript': chapter_transcript
        })

    return diarized_output

diarized_response = speaker_diarized_output(json_output)
for chapter in diarized_response:
    print(f'{chapter["chapter_summary"]} \n')
    print(f'{chapter["transcript"]} \n\n')
