
import os
from dotenv import load_dotenv

basedir:str = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

import awsgi
from src import create_app


def lambda_handler(event, context):

    app = create_app()
    return awsgi.response(app, event, context)