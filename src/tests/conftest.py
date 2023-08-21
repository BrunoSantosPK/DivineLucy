import os
from dotenv import load_dotenv


def pytest_configure(config):
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    load_dotenv(f"{base_path}/config/.env")
    

def pytest_unconfigure(config):
    pass