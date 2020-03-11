from .client import Client
from .Utils import validation
from .Utils import get_arguments
import sys


class AdvancedQueries(Client):
    """
    @namespace  MDATP
    @class      AdvancedQueries
    """
    path = "advancedqueries"

    @validation
    def run(self, Query: str) -> (dict, dict, dict):
        payload = get_arguments(locals())
        path = "{}/{}".format(self.path, sys._getframe().f_code.co_name)
        ret = self.request(path=path, payload=payload, method="post")
        return ret["Stats"], ret["Schema"], ret["Results"]
