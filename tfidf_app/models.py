from django.db import models
from django.utils import timezone


class Metrics(models.Model):
    file_name = models.CharField(max_length=256, null=False)
    processing_time = models.FloatField()
    processed_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[('error', 'Error'), ('success', 'Success')])
    memory_usage = models.FloatField()

    class Meta:
        ordering = ['-processed_timestamp']

        indexes = [models.Index(fields=['processed_timestamp'])]
