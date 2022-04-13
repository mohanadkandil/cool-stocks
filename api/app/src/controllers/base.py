from .. import adapters

class BaseController():
    def request(self, payload: dict, queryParams: dict, url: str, method: str):
        return adapters.dbAdapter.sendRequest(payload=payload, queryParams=queryParams, method=method, url=url)
