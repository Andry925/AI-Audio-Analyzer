from django.urls import path
from . import views

urlpatterns = [
    path(
        'new-task',
        views.AnalyzerTaskListView.as_view(),
        name='create-analyzer-task'),
    path(
        'view-task/<int:pk>',
        views.AnalyzerTaskDetailView.as_view(),
        name='view-analyzer-task'),
    path(
        'task-bulk-update', views.AnalyzerTaskEditView.as_view(),
        name='task-bulk-update'
    )
]
