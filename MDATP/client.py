import json
import urllib.request
import urllib.parse
import http
import http.cookiejar
from .Exception import APIException
from .Utils import get_arguments


class Client(object):
    __header: dict = dict()
    _host: str = 'https://api.securitycenter.windows.com'

    def __init__(
        self, tenantId: str = None, clientId: str = None,
        clientSecret: str = None, client: object = None
    ) -> object:
        if client is not None:
            self.__client = client.__client
            self.__header = client.__header
            self.__cookie = client.__cookie
        else:
            self.__cookie = http.cookiejar.CookieJar()
            self.__client = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(self.__cookie)
            )
            urllib.request.install_opener(self.__client)
            token = self.__createAuth(tenantId, clientId, clientSecret)
            self.__header = {
                'Content-Type': "application/json",
                'Accept': 'application/json',
                "Authorization": "Bearer {}".format(token)
            }

    def __createAuth(
        self, tenantId: str = None, clientId: str = None,
        clientSecret: str = None
    ) -> str:
        url = "https://login.windows.net/%s/oauth2/token" % (tenantId)
        body = {
            'resource': self._host,
            'client_id': clientId,
            'client_secret': clientSecret,
            'grant_type': 'client_credentials'
        }
        data = urllib.parse.urlencode(body).encode("utf-8")
        req = urllib.request.Request(url, data)
        try:
            with self.__client.open(req) as res:
#            with urllib.request.urlopen(req) as res:
                body = json.loads(res.read())
                token = body["access_token"]
                return token
        except urllib.error.HTTPError as e:
            raise APIException(e)

    def request(
        self,
        method: str = None, path: str = "",
        query: dict = None, payload: dict = None
    ) -> dict:

        url = "{}/api/{}".format(self._host, path)
        if query is not None:
            query = urllib.parse.urlencode(query)
            url = "{}/api/{}?{}".format(self._host, path, query)

        args = {
            "url": url,
            "headers": self.__header
        }
        if method is not None:
            args["method"] = method.upper()

        if payload is not None:
            payload = json.dumps(payload).encode('utf-8')
            args["data"] = payload
        req = urllib.request.Request(**args)
        try:
            with self.__client.open(req) as res:
#            with urllib.request.urlopen(req) as res:
                body = res.read().decode("utf-8")
                if body is "" or body is None:
                    return {}
                body = json.loads(body)
                return body
        except APIException as e:
            raise e
        except urllib.error.HTTPError as e:
            raise APIException(e)
