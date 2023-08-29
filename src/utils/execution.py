from flask import Response
from typing import Callable
from src.utils.transfer import Transfer


class Execution:
    @staticmethod
    def run(*args: Callable[[], Transfer]):
        for func in args:
            res = func()
            if res.get_status_code() != 200:
                break
        response = Response(res.send(), res.get_status_code())
        for d in res.get_cookies():
            response.set_cookie(d["name"], d["value"])
        return response
