from rest_framework import serializers

from .models import AnalyzerTask
from prompts.serializers import PromptSerializer


class AnalyzerTaskSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user_id.username', read_only=True)
    audio_file_url = serializers.FileField(required=False)
    prompts = PromptSerializer(many=True, read_only=True)

    class Meta:
        model = AnalyzerTask
        fields = '__all__'
