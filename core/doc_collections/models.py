from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class DocumentModel(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Collection(models.Model):
    name = models.CharField(max_length=255)
    documents = models.ManyToManyField(DocumentModel, related_name='collections')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    