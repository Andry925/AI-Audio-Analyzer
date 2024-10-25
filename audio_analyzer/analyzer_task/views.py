from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from prompts.tasks import create_llm_prompt
from .models import AnalyzerTask
from .serializers import AnalyzerTaskSerializer
from .tasks import main


class AnalyzerTaskListView(generics.ListCreateAPIView):
    serializer_class = AnalyzerTaskSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        audio_file = self.request.FILES.get('audio_file_url')
        audio_record_language = self.request.data.get('audio_file_language')
        if audio_record_language and audio_file:
            current_analyzer_task = serializer.save(
                audio_file_language=audio_record_language,
                audio_file_url=audio_file,
                user_id=self.request.user)
            main.delay(analyzer_task_id=current_analyzer_task)
        else:
            current_analyzer_task = serializer.save(user_id=self.request.user)

        create_llm_prompt.delay(current_analyzer_task.id)

    def get_queryset(self):
        queryset = AnalyzerTask.objects.filter(
            user_id=self.request.user).select_related('user_id')
        return queryset.prefetch_related('prompts')


class AnalyzerTaskDetailView(generics.RetrieveAPIView):
    serializer_class = AnalyzerTaskSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        queryset = AnalyzerTask.objects.filter(
            user_id=self.request.user).select_related('user_id')
        return queryset.prefetch_related('prompts')
