import time
import requests
from celery import shared_task
from django.db import IntegrityError
from .constants import CHUNK_SIZE, UPLOAD_ENDPOINT, HEADERS_AUTH_ONLY, TRANSCRIPT_ENDPOINT, HEADERS
from .models import AnalyzerTask

DEFAULT_TIMEOUT = 10


def upload(file_obj):
    def read_file(file_obj):
        file_obj.seek(0)
        while True:
            data = file_obj.read(CHUNK_SIZE)
            if not data:
                break
            yield data

    upload_response = requests.post(
        UPLOAD_ENDPOINT,
        headers=HEADERS_AUTH_ONLY,
        data=read_file(file_obj),
        timeout=DEFAULT_TIMEOUT
    )
    return upload_response.json()['upload_url']


def transcribe(audio_url):
    transcript_request = {
        'audio_url': audio_url,
        'language_code': 'uk'
    }

    transcript_response = requests.post(
        TRANSCRIPT_ENDPOINT,
        json=transcript_request,
        headers=HEADERS,
        timeout=DEFAULT_TIMEOUT
    )
    return transcript_response.json()['id']


def poll(transcript_id):
    polling_endpoint = TRANSCRIPT_ENDPOINT + '/' + transcript_id
    polling_response = requests.get(
        polling_endpoint,
        headers=HEADERS,
        timeout=DEFAULT_TIMEOUT
    )
    return polling_response.json()


def get_transcription_result_url(url):
    transcribe_id = transcribe(url)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        time.sleep(1)


def save_transcript(url):
    data, error = get_transcription_result_url(url)
    return data.get('text')


@shared_task
def main(analyzer_task_id):
    task = AnalyzerTask.objects.get(id=analyzer_task_id)
    audio_filename = task.audio_file_url

    audio_url = upload(audio_filename)
    extracted_text = save_transcript(audio_url)

    if extracted_text:
        task.task_text = extracted_text
        try:
            task.save()
            print("Task saved successfully.")
        except IntegrityError as e:
            print(f"Database error: {e}")
        task.refresh_from_db()
        print("Task after refresh:", task.task_text)
    else:
        print("No extracted text to save.")
