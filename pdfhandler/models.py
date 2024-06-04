# pdfhandler/models.py
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    ai_percentage = models.FloatField(default=0)  # Default AI percentage is 0

    def __str__(self):
        return self.file.name
