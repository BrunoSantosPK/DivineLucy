import json
from flask import request
from src.utils.transfer import Transfer
from src.services.wallet import WalletService


class WalletController:

    @staticmethod
    def new() -> Transfer:
        integration = Transfer()

        try:
            # Verifica o JWT enviado
            body = json.loads(request.data)
            if body["user_id"] != request.cookies.get("user_id"):
                raise Exception("Você não tem permissão para criar carteira neste usuário")
            
            wallet_id, message = WalletService.new(body["name"], body["user_id"])
            if message != "":
                raise Exception(message)
            
            integration.set_data({"wallet_id": wallet_id})

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration

    @staticmethod
    def get_all() -> Transfer:
        integration = Transfer()

        try:
            # Verifica JWT enviado
            wallets, message = WalletService.get_all(request.view_args["user_id"])
            if message != "":
                raise Exception(message)
            
            integration.set_data(wallets)

        except BaseException as e:
            integration.set_message(str(e))
            integration.set_status_code(500)

        finally:
            return integration
