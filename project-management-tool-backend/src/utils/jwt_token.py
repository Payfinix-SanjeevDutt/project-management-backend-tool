import jwt
import pytz
from datetime import datetime, timedelta
from src.config.app import FlaskEnv

def generate_token(**kwargs):
    """Generate a token for the given user."""
    
    timezone = pytz.timezone("Asia/Kolkata")
    exp_time = datetime.now(tz=timezone) + timedelta(days=3)
    nbf_time = datetime.now(tz=timezone)

    data = {
        **kwargs,
        'exp' : exp_time,
        'nbf':nbf_time
    }
    encoded_jwt = jwt.encode(
        data,
        FlaskEnv.SECRET_KEY, 
        algorithm="HS256"
    )

    return encoded_jwt


def decode_token(token):
    decoded_data = jwt.decode(token, FlaskEnv.SECRET_KEY, algorithms=["HS256"])
    return decoded_data