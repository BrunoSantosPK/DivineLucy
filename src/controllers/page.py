from flask import render_template
from src.utils.transfer import Transfer


class PageController:
    @staticmethod
    def to_login(status_code: int=200) -> Transfer:
        res = Transfer()
        res.set_status_code(status_code)
        res.set_html(render_template("login.html"))
        return res
    
    @staticmethod
    def to_home() -> Transfer:
        res = Transfer()
        res.set_html(render_template("index.html"))
        return res
    
    @staticmethod
    def to_budget() -> Transfer:
        res = Transfer()
        res.set_html(render_template("budget.html"))
        return res
    
    @staticmethod
    def to_transactions() -> Transfer:
        res = Transfer()
        res.set_html(render_template("transaction.html"))
        return res
    
    @staticmethod
    def to_404(message: str) -> Transfer:
        res = Transfer()
        res.set_status_code(404)
        res.set_html(render_template("404.html", message=message))
        return res
    
    @staticmethod
    def to_recover(recover_id: str) -> Transfer:
        res = Transfer()
        res.set_html(render_template("recover.html", recover=recover_id))
        return res
