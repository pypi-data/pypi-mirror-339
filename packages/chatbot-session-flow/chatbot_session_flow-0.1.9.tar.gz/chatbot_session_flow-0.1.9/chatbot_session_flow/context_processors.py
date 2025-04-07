from chatbot_session_flow.models import *

def menu_links(request):
    links = Profile.objects.all()
    return dict(links=links)