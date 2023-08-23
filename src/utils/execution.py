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
        return Response(res.send(), res.get_status_code())
