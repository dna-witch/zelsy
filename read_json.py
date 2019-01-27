import json

with open('tone.json', 'r') as f:
    tone_dict = json.load(f)

for tone in tone_dict['sentences_tone']:
    print(tone['tones'][0]['tone_id'])