from analyzer_task.models import AnalyzerTask
from django.db import models


class Prompt(models.Model):
    prompt_content = models.TextField()
    task_id = models.ForeignKey(AnalyzerTask, on_delete=models.CASCADE, related_name='prompts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.prompt_content}'
