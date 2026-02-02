from django.urls import path
from .views import ChatMessageAPIView

urlpatterns = [
    path("chat/messages/", ChatMessageAPIView.as_view()),
]


