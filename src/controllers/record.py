import json
from flask import request
from src.utils.transfer import Transfer
from src.services.record import RecordService, RecordDetails


class RecordController:

    @staticmethod
    def get_all() -> Transfer:
        integration = Transfer()

        try:
            # Verifica JWT enviado
            user_id = request.view_args["user_id"]
            page = int(request.args.get("page", default=1))
            res = RecordService.get_all(user_id, page=page)
            if not res.success:
                raise Exception(res.message)
            
            integration.set_data(res.records)

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
            # Avalia campos opcionais
            body = json.loads(request.data)
            if "details" not in body.keys():
                body["details"] = []
            if "origin_id" not in body.keys():
                body["origin_id"] = None

            # Transforma lista de detalhes
            for i in range(0, len(body["details"])):
                body["details"][i] = RecordDetails(body["details"][i]["description"], body["details"][i]["value"])

            res = RecordService.new(
                body["user_id"],
                body["item_id"],
                body["target_id"],
                body["moviment_date"],
                body["description"],
                body["value"],
                origin_id=body["origin_id"],
                details=body["details"]
            )
            if not res.success:
                raise Exception(res.message)
            integration.set_data({"record_id": res.record_id})

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
            # Avalia campos opcionais
            body = json.loads(request.data)
            if "details" not in body.keys():
                body["details"] = []
            if "origin_id" not in body.keys():
                body["origin_id"] = None

            # Transforma lista de detalhes
            for i in range(0, len(body["details"])):
                body["details"][i] = RecordDetails(body["details"][i]["description"], body["details"][i]["value"])

            # Faz a atualização
            res = RecordService.edit(
                body["record_id"],
                body["user_id"],
                body["item_id"],
                body["target_id"],
                body["moviment_date"],
                body["description"],
                body["value"],
                origin_id=body["origin_id"],
                details=body["details"]
            )
            if not res.success:
                raise Exception(res.message)

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
            res = RecordService.delete(body["record_id"], body["user_id"])
            if not res.success:
                raise Exception(res.message)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration
