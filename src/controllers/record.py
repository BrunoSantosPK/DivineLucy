import json
from flask import request
from src.utils.transfer import Transfer
from src.services.record import RecordService


class RecordController:

    @staticmethod
    def get_all() -> Transfer:
        integration = Transfer()

        try:
            # Verifica JWT enviado
            user_id = request.view_args["user_id"]
            page = int(request.args.get("page", default=1))

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration

    @staticmethod
    def new() -> Transfer:
        integration = Transfer()

        try:
            # Verifica JWT enviado
            body = json.loads(request.data)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration

    @staticmethod
    def edit() -> Transfer:
        integration = Transfer()

        try:
            # Verifica JWT enviado
            body = json.loads(request.data)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration

    @staticmethod
    def delete() -> Transfer:
        integration = Transfer()

        try:
            # Verifica JWT enviado
            body = json.loads(request.data)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration
