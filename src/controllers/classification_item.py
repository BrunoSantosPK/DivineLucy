import json
from flask import request
from src.utils.transfer import Transfer
from src.services.classification_item import ClassificationItemService


class ClassificationItemController:

    @staticmethod
    def new():
        integration = Transfer()

        try:
            # Verifica JWT enviado
            body = json.loads(request.data)
            item_id, message = ClassificationItemService.new(body["user_id"], body["name"])
            if message != "":
                raise Exception(message)
            
            integration.set_data({"item_id": item_id})

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration

    @staticmethod
    def get_all():
        integration = Transfer()

        try:
            # Verifica JWT enviado
            user_id = request.view_args["user_id"]
            items, message = ClassificationItemService.get_all(user_id)
            if message != "":
                raise Exception(message)
            
            integration.set_data(items)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration
        
    @staticmethod
    def delete():
        integration = Transfer()

        try:
            # Verifica JWT enviado
            body = json.loads(request.data)
            message = ClassificationItemService.delete(body["item_id"], body["user_id"])
            if message != "":
                raise Exception(message)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration
