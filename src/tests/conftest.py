import os
from dotenv import load_dotenv


# TODO: incluir aqui a criação do usuário padrão.
# Atualmente o padrão é bruno.19ls@gmail.com / Lambaroso1
# TODO: incluir um recover_id padrão para ser utilizado
# Atualmente o padrão é a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11
def pytest_configure(config):
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    load_dotenv(f"{base_path}/config/.env")
    

def pytest_unconfigure(config):
    pass