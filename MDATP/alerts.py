from .client import Client
from .Utils import validation
from .Utils import get_arguments


class Alerts(Client):
    """
    @namespace  MDATP
    @class      Alerts
    """
    path = "alerts"

    def list(self,):
        response = self.request(method="get", path=self.path)
        return response
