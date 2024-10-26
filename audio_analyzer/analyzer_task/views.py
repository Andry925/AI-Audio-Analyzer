from django.core.exceptions import ValidationError
from prompts.tasks import create_llm_prompt
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import AnalyzerTask
from .serializers import AnalyzerTaskSerializer, AnalyzerTaskEditSerializer
from .tasks import run_audio_transcription
from rest_framework.pagination import PageNumberPagination


class AudioCustomPaginator(PageNumberPagination):
    page_size = 5

class AnalyzerTaskListView(generics.ListCreateAPIView):
    serializer_class = AnalyzerTaskSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = AudioCustomPaginator

    def perform_create(self, serializer):
        audio_file = self.request.FILES.get('audio_file_url')
        audio_record_language = self.request.data.get('audio_file_language')
        if audio_record_language and audio_file:
            current_analyzer_task = serializer.save(
                audio_file_language=audio_record_language,
                audio_file_url=audio_file,
                user_id=self.request.user)
            run_audio_transcription(
                analyzer_task_id=current_analyzer_task.id,
                audio_file_language=audio_record_language)
        else:
            current_analyzer_task = serializer.save(user_id=self.request.user)

        create_llm_prompt(current_analyzer_task.id)

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


class AnalyzerTaskEditView(generics.UpdateAPIView):
    serializer_class = AnalyzerTaskEditSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data'), list):
            kwargs["many"] = True
            return super().get_serializer(*args, **kwargs)

    def get_queryset(self, ids=None):
        if ids:
            queryset = AnalyzerTask.objects.filter(
                id__in=ids,
                user_id=self.request.user).select_related('user_id').prefetch_related('prompts')
        else:
            queryset = AnalyzerTask.objects.filter(
                user_id=self.request.user).select_related('user_id').prefetch_related('prompts')
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        ids = self.validate_ids(request.data)

        instances = self.get_queryset(ids=ids)

        serializer = self.get_serializer(
            instances, data=request.data, partial=True, many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    @staticmethod
    def validate_ids(data, field="id", unique=True):
        if isinstance(data, list):
            id_list = [int(x[field]) for x in data]

            if unique and len(id_list) != len(set(id_list)):
                raise ValidationError(
                    "Multiple updates to a single {} found".format(field))

            return id_list

        return [data]


class AnalyzerTaskRemoveView(generics.DestroyAPIView):
    serializer_class = AnalyzerTaskEditSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        queryset = AnalyzerTask.objects.filter(
            user_id=self.request.user).select_related('user_id')
        return queryset.prefetch_related('prompts')

    def destroy(self, request, *args, **kwargs):
        ids = request.data.get("ids")
        if not isinstance(
                ids,
                list) or not all(
                isinstance(
                id,
                int) for id in ids):
            return Response({"detail": "provide correct ids list"},
                            status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset().filter(id__in=ids)
        queryset.delete()
        return Response({"detail": "deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)
