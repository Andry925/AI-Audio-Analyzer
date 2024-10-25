from decouple import config

UPLOAD_ENDPOINT = 'https://api.assemblyai.com/v2/upload'
TRANSCRIPT_ENDPOINT = 'https://api.assemblyai.com/v2/transcript'

HEADERS_AUTH_ONLY = {'authorization': config('API_KEY_ASSEMBLYAI')}

HEADERS = {
    "authorization": config('API_KEY_ASSEMBLYAI'),
    "content-type": "application/json"
}

CHUNK_SIZE = 5_242_880
