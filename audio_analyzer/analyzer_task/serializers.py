from django.core.exceptions import ValidationError
from django.db import IntegrityError
from prompts.serializers import PromptSerializer
from rest_framework import serializers

from .models import AnalyzerTask


class AnalyzerTaskSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user_id.username', read_only=True)
    audio_file_url = serializers.FileField(required=False)
    prompts = PromptSerializer(many=True, read_only=True)

    class Meta:
        model = AnalyzerTask
        fields = '__all__'


class AnalyzerTaskBulkUpdateSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        instance_dict = {instance.id: instance for instance in instance}
        result = []
        for attrs in validated_data:
            instance = instance_dict.get(attrs['id'])
            if instance:
                for attr, value in attrs.items():
                    setattr(instance, attr, value)
                result.append(instance)

        concrete_fields = [
            field.name for field in self.child.Meta.model._meta.get_fields()
            if not (field.is_relation or field.auto_created)
        ]
        writable_fields = [
            x for x in self.child.Meta.fields if x in concrete_fields
        ]

        try:
            self.child.Meta.model.objects.bulk_update(result, writable_fields)
        except IntegrityError as e:
            raise ValidationError(e)

        return result


class AnalyzerTaskEditSerializer(serializers.ModelSerializer):
    prompts = PromptSerializer(many=True, read_only=True)
    id = serializers.IntegerField()

    class Meta:
        model = AnalyzerTask
        fields = ['id', 'name', 'prompts']
        list_serializer_class = AnalyzerTaskBulkUpdateSerializer


