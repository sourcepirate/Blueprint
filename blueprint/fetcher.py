"""Fetcher.py"""

import json
import requests

class BluePrintException(Exception):
    """Blueprint base exception"""

    def __init__(self, message):
        self.message = message
        super(BluePrintException, self).__init__()

    def __str__(self):
        return str(self.message)


class Fetcher(dict):
    """Fetches Resource from url"""
    
    _headers = {"Content-type": "application/json"}
    _serializer = json.dumps

    def __init__(self, url, method="GET", payload={}, headers={}):

        self._url = url
        self._method = method
        self._headers.update(headers)
        _payload = {}
        if self._method.lower() == "GET":
            _payload.update({"params": self._serializer(payload)})
        else:
            _payload.update({"data": self._serializer(payload)})
        super(Fetcher, self).__init__(_payload)

    def execute(self):
        _method = getattr(requests, self._method.lower())
        response = _method(self._url, headers=self._headers, **self)
        try:
            return response.json()
        except:
            raise BluePrintException("Cannot decode JSON response")