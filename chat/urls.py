from django.contrib import admin
from django.urls import path
from .views import chatbot_response,chat_view

urlpatterns = [
      path('api/chatbot/', chatbot_response, name='chatbot_response'),
      path('chat/', chat_view, name='chat'),

]
