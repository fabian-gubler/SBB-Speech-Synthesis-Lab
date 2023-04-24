import requests
import time

API_KEY = '<YOUR_API_KEY>'  # Get your API key here: https://app.fliki.ai/account/api
API_URL = 'https://api.fliki.ai/v1'

def api(method, endpoint, params=None):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    url = f'{API_URL}{endpoint}'
    try:
        response = requests.request(method, url, headers=headers, json=params)
        response.raise_for_status()
        return response.json().get('data')
    except Exception as error:
        print(error)
        return None


# Get languages
languages = api('GET', '/languages')
print('languages', languages)

# Get dialects
# dialects = api('GET', '/dialects')
# print('dialects', dialects)

# Get voices
# voices = api('POST', '/voices', params={
#     'languageId': '61b8b2f54268666c126babc9',  # English
#     'dialectId': '61b8b31c4268666c126bace7',  # United States
# })
# print('voices', voices)

# Generate
# generate = api('POST', '/generate', params={
#     'format': 'video',
#     'scenes': [
#         {
#             'content': 'Eating at regular times during the day helps burn calories at a faster rate and reduces the temptation to snack on foods high in fat and sugar.',
#             'voiceId': '61b8b45a4268666c126bb32b',  # English, United States, Sara
#         },
#         {
#             'content': 'Fruit and vegetables are low in calories and fat and they also contain plenty of vitamins and minerals.',
#             'voiceId': '61b8b45a4268666c126bb32b',  # English, United States, Sara
#         },
#     ],
#     'settings': {
#         'aspectRatio': 'portrait',
#         'subtitle': {
#             'fontColor': 'yellow',
#             'backgroundColor': 'black',
#             'placement': 'bottom',
#             'display': 'phrase',
#         },
#     },
#     'backgroundMusicKeywords': 'happy, lofi, beats',
# })

# print('generate', generate)

# Generate status
# def check_status(id):
#     status = api('POST', '/generate/status', params={'id': id})
#     print('status', status)

#     if status and status['status'] == 'processing':
#         time.sleep(5)
#         return check_status(id)

#     return status

# id = '<ID>'
# check_status(id)

# Generate text-to-speech
# audio = api('POST', '/generate/text-to-speech', params={
#     'content': 'Hello, thank you for giving Fliki API a try!',
#     'voiceId': '61b8b45a4268666c126bb32b',  # English, United States, Sara
# })

# print('audio', audio)
