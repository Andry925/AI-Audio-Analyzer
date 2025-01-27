# Generated by Django 5.1.2 on 2024-10-24 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analyzer_task', '0005_alter_analyzertask_task_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prompts', to='analyzer_task.analyzertask')),
            ],
        ),
    ]
