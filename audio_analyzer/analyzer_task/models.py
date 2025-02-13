from django.conf import settings
from django.db import models

DEFAULT_MIDJOURNEY_FORMULA = (
    "subject description",
    "5 descriptive keywords",
    "camera type",
    "camera lens type",
    "time of day",
    "style of photograph",
    "type of film")


def upload_to(instance, filename):
    return f'audios/{filename}'


class AnalyzerTask(models.Model):
    AUDIO_LANGUAGE_CHOICES = [
        ('uk', 'uk'),
        ('en', 'en'),
        ('ru', 'ru'),
    ]

    name = models.TextField(max_length=255)
    # You can add more languages but by default there are three
    audio_file_url = models.FileField(
        upload_to=upload_to, null=True, blank=True)
    audio_file_language = models.TextField(
        max_length=20,
        choices=AUDIO_LANGUAGE_CHOICES,
        null=True,
        blank=True
    )
    task_text = models.TextField(blank=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    helper_instruction = models.TextField(
        null=True,
        blank=True,
        default=DEFAULT_MIDJOURNEY_FORMULA
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
