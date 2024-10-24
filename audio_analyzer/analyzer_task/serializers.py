from rest_framework import serializers

from .models import AnalyzerTask


class AnalyzerTaskSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user.username', read_only=True)
    audio_file_url = serializers.FileField(required=False)

    class Meta:
        model = AnalyzerTask
        fields = '__all__'
