from flask import Flask
from .app import FlaskEnv


def initconfig(app: Flask):
    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=FlaskEnv.DB_TRACK_MODIFICATIONS,
        SQLALCHEMY_DATABASE_URI=FlaskEnv.DATABASE_URI,
        SQLALCHEMY_POOL_SIZE = FlaskEnv.SQLALCHEMY_POOL_SIZE,
        SQLALCHEMY_MAX_OVERFLOW = FlaskEnv.SQLALCHEMY_MAX_OVERFLOW,
        SQLALCHEMY_POOL_TIMEOUT = FlaskEnv.SQLALCHEMY_POOL_TIMEOUT,
        SQLALCHEMY_POOL_RECYCLE = FlaskEnv.SQLALCHEMY_POOL_RECYCLE,
        SQLALCHEMY_POOL_PRE_PING =  FlaskEnv.SQLALCHEMY_POOL_PRE_PING,
        SECRET_KEY = FlaskEnv.SECRET_KEY
    )

from .sharepoint import SharePointApi