from django.conf import settings
from django.db import models


def upload_to(instance, filename):
    return f'audios/{filename}'


class AnalyzerTask(models.Model):
    name = models.CharField(max_length=255)
    audio_file_url = models.FileField(
        upload_to=upload_to, null=True, blank=True)
    audio_file_language = models.CharField(
        max_length=255, null=True, blank=True)
    task_text = models.TextField(blank=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks')
    helper_instruction = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
