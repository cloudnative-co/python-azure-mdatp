import urllib
import json


class APIException(urllib.error.HTTPError):

    def __init__(self, e: urllib.error.HTTPError = None):
        super()
        if e is not None:
            self.state = e.code
            self.hdrs = e.hdrs
            self.fp = e.fp
            self.filename = e.filename
            self.code = e.code
            self.msg = e.msg
            body = e.read().decode("utf-8")
            try:
                body = json.loads(body)
                error = body.get("error", None)
                if isinstance(error, dict):
                    self.msg = error.get("message", e.msg)
                    self.code = error.get("code", e.code)
                    if self.msg == "":
                        self.msg = e.msg
                elif isinstance(error, str):
                    msg = body.get("error_description", None)
                    msg = msg.split("\r\n")
                    self.msg = msg[0]
                    self.code = body.get("error_codes", None)[0]
                    self.filename = body.get("error_uri", None)
                    self.timestamp = body.get('timestamp', None)
                    self.trace_id = body.get('trace_id', None)
                    self.correlation_id = body.get('correlation_id', None)
            except json.JSONDecodeError as e:
                pass

    def __str__(self):
        return json.dumps({
            "message": self.msg,
            "code": self.code,
            "status": self.state,
            "uri": self.filename
        })
