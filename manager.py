import os
import sys
from dotenv import load_dotenv
import src.database.actions as actions


def create() -> None:
    actions.create_tables()


def delete() -> None:
    actions.delete_tables()


def seed() -> None:
    actions.create_root_user()
    actions.create_default_items()


def wallets() -> None:
    actions.create_test_wallets()


def pipe() -> None:
    delete()
    create()
    seed()


if __name__ == "__main__":
    # Define path do projeto e carrega variáveis de ambiente
    base_path = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(f"{base_path}/config/.env")
    
    
    # Faz a chamada da função passada como parâmetro
    available = ["create", "delete", "seed", "pipe", "wallets"]
    args = sys.argv
    if len(args) != 2:
        raise Exception("Comando inválido, utilize sempre python manager.py <nome_da_funcao>.")

    if args[1] not in available:
        raise Exception(f"Função não encontrada. Estão disponíveis: {', '.join(available)}")
    
    globals()[args[1]]()