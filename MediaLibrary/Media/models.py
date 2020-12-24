from django.db import models
import uuid


class Media(models.Model):
    class Meta:
        db_table = 'Media'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media_id = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    media_name = models.CharField(max_length=30)
    media_type = models.CharField(max_length=10)

    def __str__(self):
        return self.media_name
