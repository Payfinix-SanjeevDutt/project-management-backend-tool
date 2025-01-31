from .loadenv import get_env_variable


class FlaskEnv:
    
    DB_TRACK_MODIFICATIONS:bool = False if get_env_variable('DB_TRACK_MODIFICATIONS') == "false" else True
    DATABASE_URI:str = get_env_variable("DATABASE_URI")
    SECRET_KEY:str = get_env_variable("SECRET_KEY")
    SQLALCHEMY_POOL_SIZE:int = int(get_env_variable("SQLALCHEMY_POOL_SIZE")) # The size of the database connection pool
    SQLALCHEMY_MAX_OVERFLOW:int = int(get_env_variable("SQLALCHEMY_MAX_OVERFLOW")) # The maximum overflow size of the connection pool
    SQLALCHEMY_POOL_TIMEOUT:int = int(get_env_variable("SQLALCHEMY_POOL_TIMEOUT")) # The number of seconds to wait before giving up on getting a connection from the pool
    SQLALCHEMY_POOL_RECYCLE:int = int(get_env_variable("SQLALCHEMY_POOL_RECYCLE"))  # The number of seconds a connection can persist before being recycled
    SQLALCHEMY_POOL_PRE_PING:bool = False if get_env_variable("SQLALCHEMY_POOL_PRE_PING")=="false" else True # If set to True, the connection pool will test connections for liveness
