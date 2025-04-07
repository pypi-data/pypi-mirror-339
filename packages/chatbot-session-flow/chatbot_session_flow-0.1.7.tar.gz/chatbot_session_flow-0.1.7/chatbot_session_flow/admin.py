from django.contrib import admin
from chatbot_session_flow.models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Session)
admin.site.register(Page)
admin.site.register(PageOption)
admin.site.register(Stepper)
admin.site.register(CollectedData)