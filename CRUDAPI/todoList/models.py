from django.db import models
from datetime import datetime

class Todo(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=400, null=False)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.utcnow)

    def __str__(self) -> str:
        return self.name
