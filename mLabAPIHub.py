import requests

class mLabAPIHub(object):

    API_Hub_URL = 'https://apihub.hdanny.org/api_hub'

    def __init__(self, mlab_key: str):
        self._mlab_key = mlab_key

    def call_api(self, api_call, **params):
        return requests.post(
            f'{mLabAPIHub.API_Hub_URL}/{api_call}/',
            json=dict(mlab_key=self._mlab_key, params=params)
        ).json()