import json
from flask import request
from src.utils.transfer import Transfer
from src.services.budget import BudgetService


class BudgetController:

    @staticmethod
    def new() -> Transfer:
        integration = Transfer()

        try:
            body = json.loads(request.data)
            if body["user_id"] != request.cookies.get("user_id"):
                raise Exception("Você não tem permissão para criar meta neste usuário")
            
            budget_id, message = BudgetService.new(
                body["user_id"], body["year"], body["month"],
                body["item_id"], body["value"]
            )
            if message != "":
                raise Exception(message)
            
            integration.set_data({"budget_id": budget_id})

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration

    @staticmethod
    def edit() -> Transfer:
        integration = Transfer()

        try:
            body = json.loads(request.data)
            if body["user_id"] != request.cookies.get("user_id"):
                raise Exception("Você não tem permissão para editar esta meta")
            
            message = BudgetService.edit(body["budget_id"], body["item_id"], body["value"])
            if message != "":
                raise Exception(message)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration
        
    @staticmethod
    def get_all() -> Transfer:
        integration = Transfer()

        try:
            user_id = request.view_args["user_id"]
            month = int(request.args.get("month"))
            year = int(request.args.get("year"))

            if user_id != request.cookies.get("user_id"):
                raise Exception("Você não tem permissão para visualizar dados do usuário solicitado")

            data, message = BudgetService.get_all(user_id, year, month)
            if message != "":
                raise Exception(message)
            
            integration.set_data(data)
            
        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration

    @staticmethod
    def delete() -> Transfer:
        integration = Transfer()

        try:
            body = json.loads(request.data)
            user_id = request.cookies.get("user_id")
            result, message = BudgetService.delete(body["budget_id"], user_id)
            if message != "":
                raise Exception(message)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration