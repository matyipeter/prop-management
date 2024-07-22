from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

@login_required
def chat(request):
    users = User.objects.exclude(username=request.user.username)
    print(users)
    return render(request, 'messaging/chat.html', {'users': users})

@login_required
def chat_room(request, username):
    other_user = User.objects.get(username=username)
    messages = Message.objects.filter(sender=request.user, recipient=other_user) | Message.objects.filter(sender=other_user, recipient=request.user)
    return render(request, 'messaging/chatPage.html', {'other_user': other_user, 'messages': messages})