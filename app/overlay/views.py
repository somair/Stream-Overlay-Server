from django.shortcuts import render
from django.shortcuts import redirect
from os import environ
import requests

def index(request):
    url = 'https://api.twitch.tv/kraken/oauth2/authorize'
    url = url + '?client_id=' + environ.get('client_id')
    url = url + '&redirect_uri=http://localhost:8000/overlay/api_redirect'
    url = url + '&scope=channel_subscriptions+viewing_activity_read'
    url = url + '&response_type=code'
    return redirect(url)

def api_redirect(request):
    print('---------------------- IN REDIRECT --------------------')
    print(request.POST)
    if request.GET.get('access_token', None) is None:
        data = {
            'client_id': environ.get('client_id'),
            'client_secret': environ.get('client_secret'),
            'code': request.GET.get('code'),
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:8000/overlay/api_redirect',
            'state': request.GET.get('state')
        }
        requests.post('https://api.twitch.tv/kraken/token', data=data)

        context = {}
        return render(request, 'overlay/index.html', context)
    return redirect('https://www.google.com')

# def api_redirect(request):
#     print('---------------------- IN REDIRECT --------------------')
#     if request.GET.get('access_token', None) is None:
#
#         url = 'https://api.twitch.tv/kraken/oauth2/token'
#         url = url + '?client_id=' + environ.get('client_id')
#         url = url + '&client_secret=' + environ.get('client_secret')
#         url = url + '&code=' + request.GET.get('code')
#         url = url + '&grant_type=authorization_code'
#         url = url + '&redirect_uri=http://localhost:8000/overlay/api_redirect'
#         print(url)
#         return redirect(url)
#     else:
#         print(request)
#         context = {}
#         return render(request, 'overlay/index.html', context)