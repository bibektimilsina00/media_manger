from django.db import models

class MediaFile(models.Model):
    CATEGORY_CHOICES = [
        ('AUDIO', 'Audio'),
        ('VIDEO', 'Video'),
        ('IMAGE', 'Image'),
    ]
    
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=255)
    size = models.IntegerField()  # in bytes
    file_type = models.CharField(max_length=10)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name