import json
from typing import Any, List


class Transfer:
    def __init__(self) -> None:
        self.__message = ""
        self.__status_code = 200
        self.__data = None
        self.__html: str = None
        self.__cookies: List[dict] = []

    def set_data(self, data) -> None:
        self.__data = data

    def set_status_code(self, status_code: int) -> None:
        self.__status_code = status_code

    def set_message(self, message: str) -> None:
        self.__message = message

    def set_cookie(self, name: str, value: str) -> None:
        self.__cookies.append({"name": name, "value": value})

    def set_html(self, template: str):
        self.__html = template

    def get_status_code(self) -> int:
        return self.__status_code
    
    def get_message(self) -> str:
        return self.__message
    
    def get_data(self) -> Any:
        return self.__data
    
    def get_cookies(self) -> List[dict]:
        return self.__cookies
    
    def send(self) -> str:
        if self.__html is not None:
            return self.__html
        else:
            return self.to_json()

    def to_json(self) -> str:
        return json.dumps({
            "status_code": self.__status_code,
            "message": self.__message,
            "data": self.__data
        })
