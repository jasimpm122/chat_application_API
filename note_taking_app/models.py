from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Note(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_notes')
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)
    shared_users = models.ManyToManyField(User, related_name='shared_notes')

    def __str__(self):
        return self.content


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateTimeField(default=timezone.now())


class Share(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
