from rest_framework import viewsets

from tasks.models import Task
from tasks.serializer import TaskSerializer


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
