# Generated by Django 5.1.2 on 2024-10-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer_task', '0006_alter_analyzertask_helper_instruction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyzertask',
            name='audio_file_language',
            field=models.TextField(blank=True, choices=[('uk', 'uk'), ('eng', 'eng'), ('rus', 'rus')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='analyzertask',
            name='name',
            field=models.TextField(max_length=255),
        ),
    ]
