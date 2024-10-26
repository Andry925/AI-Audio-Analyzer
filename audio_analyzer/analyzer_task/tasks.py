import time

import requests
from django.db import IntegrityError

from .constants import CHUNK_SIZE, UPLOAD_ENDPOINT, HEADERS_AUTH_ONLY, TRANSCRIPT_ENDPOINT, HEADERS
from .models import AnalyzerTask

DEFAULT_TIMEOUT = 10


def upload(file_obj):
    def read_file(file_obj):
        file_obj.seek(0)
        while chunk := file_obj.read(CHUNK_SIZE):
            yield chunk

    response = requests.post(
        UPLOAD_ENDPOINT,
        headers=HEADERS_AUTH_ONLY,
        data=read_file(file_obj),
        timeout=DEFAULT_TIMEOUT
    )
    return response.json().get('upload_url')


def transcribe(audio_url, audio_language):
    transcript_request = {
        'audio_url': audio_url,
        'language_code': 'uk'
    }
    response = requests.post(
        TRANSCRIPT_ENDPOINT,
        json=transcript_request,
        headers=HEADERS,
        timeout=DEFAULT_TIMEOUT
    )
    return response.json().get('id')


def poll_transcription(transcript_id):
    polling_endpoint = f"{TRANSCRIPT_ENDPOINT}/{transcript_id}"
    while True:
        response = requests.get(
            polling_endpoint,
            headers=HEADERS,
            timeout=DEFAULT_TIMEOUT
        )
        data = response.json()
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data.get('error')
        time.sleep(1)


def get_transcription_text(audio_url, audio_language):
    transcribe_id = transcribe(audio_url, audio_language)
    data, error = poll_transcription(transcribe_id)
    if error:
        print(f"Transcription error: {error}")
    return data.get('text')


def process_transcription(task, audio_file_language):
    audio_url = upload(task.audio_file_url)

    transcribed_text = get_transcription_text(audio_url, audio_file_language)

    if transcribed_text:
        task.task_text = transcribed_text
        try:
            task.save()
            print("Task saved successfully.")
        except IntegrityError as e:
            print(f"Database error: {e}")
        task.refresh_from_db()
        print("Task after refresh:", task.task_text)
    else:
        print("No extracted text to save.")


def run_audio_transcription(analyzer_task_id, audio_file_language):
    task = AnalyzerTask.objects.get(id=analyzer_task_id)
    process_transcription(task, audio_file_language)
