from requests_futures.sessions import FuturesSession

class dbDoctor():
    def __init__(self):
        self.session = FuturesSession()
        self.db_hostname = 'http://127.0.0.1:80'


    def sendRequest(self, payload: dict, queryParams, method, url) -> Any:
        params: dict = queryParams
        if method == 'post':
            response = self.session.post(f'{self.db_hostname}/db/{url}', params=params, json=payload)
            res = response.result()
        if (res.status_code != 200 and res.status_code != 201):
            print('DB error ...', res.status_code)
            raise Exception('db error ...')
        return res.json()

dbDoctor = dbDoctor()
