from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.content[:20]}"


class Room(models.Model):
    WAITING = "waiting"
    ACTIVE = "active"
    CLOSED = "closed"

    CHOICE_STATUS = (
        (WAITING, "Waiting"),
        (ACTIVE, "Active"),
        (CLOSED, "Closed"),
    )

    uuid = models.CharField(max_length=255, unique=True)
    client = models.CharField(max_length=255)
    agent = models.ForeignKey(User, related_name='rooms', blank=True, null=True, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message, related_name='rooms', blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=CHOICE_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.uuid