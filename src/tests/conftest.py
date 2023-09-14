import os
from dotenv import load_dotenv


# TODO: incluir aqui a criação do usuário padrão.
# Atualmente o padrão é bruno.19ls@gmail.com / Lambaroso1 / b334d4ee-b95a-462e-bc7a-b19ec2e242dd
# TODO: incluir um recover_id padrão para ser utilizado
# Atualmente o padrão é a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11
# TODO: incluir itens de classificação e carteira padrões para testes de transações
# Item Supermercado fb0b8338-63ab-4ccf-8ebf-8e4b2798b08a
# Carteira Poupança 24d3bbbc-20a2-4350-bf96-408501af4a4b
# Carteira Física 7961fd02-ac54-458a-a9ae-e3d57241aa70
def pytest_configure(config):
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    load_dotenv(f"{base_path}/config/.env")
    

def pytest_unconfigure(config):
    pass