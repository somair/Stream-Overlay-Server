from django.shortcuts import render
from django.shortcuts import redirect
from os import environ
import requests

def get_access_token(code):
    data = {
        'client_id': environ.get('client_id'),
        'client_secret': environ.get('client_secret'),
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8000/overlay/api_redirect'
    }
    response = requests.post('https://api.twitch.tv/kraken/oauth2/token', params=data)
    return response.json()['access_token']

def get_channel_info(access_token):
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+jso',
        'Client-ID': environ.get('client_id'),
        'Authorization': 'OAuth ' + access_token
    }
    response = requests.get('https://api.twitch.tv/kraken/channel', headers=headers)
    return response.json()

def get_channel_follows(channel_id):
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+jso',
        'Client-ID': environ.get('client_id')
    }
    url = 'https://api.twitch.tv/kraken/channels/' + channel_id + '/follows'
    response = requests.get(url, headers=headers)
    return response.json()['follows']


def index(request):
    url = 'https://api.twitch.tv/kraken/oauth2/authorize'
    url = url + '?client_id=' + environ.get('client_id')
    url = url + '&redirect_uri=http://localhost:8000/overlay/api_redirect'
    url = url + '&scope=channel_subscriptions+channel_read+viewing_activity_read'
    url = url + '&response_type=code'

    return redirect(url)

def api_redirect(request):
    access_token = get_access_token(request.GET.get('code'))
    channel_info = get_channel_info(access_token)
    channel_follows = get_channel_follows(channel_info['_id'])

    context = {
        'channel': channel_info,
        'channel_follows': channel_follows
    }
    return render(request, 'overlay/index.html', context)
