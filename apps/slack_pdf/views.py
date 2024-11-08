from rest_framework.views import APIView
from slack_bolt.adapter.django import SlackRequestHandler
from .slack_listeners import app
handler = SlackRequestHandler(app=app)

class Slack_Events_Handler(APIView):
    def post(self, request):
        
        return handler.handle(request)
