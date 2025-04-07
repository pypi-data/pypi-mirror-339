from django.urls import re_path
from . import views
from chatbot_session_flow.views import *

urlpatterns = [
    re_path('sendTestMessage', views.sendWhatsappMessageViaNgumzo),
    re_path('messageCallback', views.messageCallback),
]
