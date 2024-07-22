from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.chat, name="chat"),
    path("<str:username>/", views.chat_room, name="chat_room"),
]