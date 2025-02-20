import os
from dotenv import load_dotenv

basedir:str = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


from src import create_app

app = create_app()