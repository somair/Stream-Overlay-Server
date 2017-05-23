from django.shortcuts import render
import requests

def index(request):
    # Currently using an alternative API to get twitch info with authentication
    # Need to figure out how to authenticate with the proper API
    response = requests.get("https://wind-bow.gomix.me/twitch-api/channels/alyxdelunar/follows")
    context = {
        'data': response.json()
    }
    return render(request, 'overlay/index.html', context)