from fastapi import HTTPException
from requests_futures.sessions import FuturesSession
from typing import Any

from ..config import settings

db_url = settings.DB_URL

class dbAdapter():
    def __init__(self):
        self.session = FuturesSession()
        self.db_hostname = f'http://{db_url}'

    def errorGeneration(self, res) -> Any:
        print('DB error ...', res.status_code)
        if res.status_code == 422:
            raise HTTPException(status_code=400, detail=f'Bad Request')
        if res.status_code == 500:
            raise Exception(f'database error return {res.status_code}, {res.content}')

    def sendRequest(self, payload: dict, queryParams, method, url) -> Any:
        params: dict = queryParams
        if method == 'get':
            response = self.session.get(f'{self.db_hostname}/db/{url}', params=params)
        elif method == 'post':
            response = self.session.post(f'{self.db_hostname}/db/{url}', params=params, json=payload)
        elif method == 'put':
            response = self.session.put(f'{self.db_hostname}/db/{url}', params=params, json=payload)

        try:
            res = response.result()
        except Exception as err:
            raise Exception(err)
        if (res.status_code != 200 and res.status_code != 201):
            self.errorGeneration(res)
        return res.json()

dbAdapter = dbAdapter()
