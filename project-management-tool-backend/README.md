# project-management-tool-backend


# Requirements

    python 3.11


# Run

Create virtual env

    py -m venv venv

navigate and activate virtual env

    .\venv\Scripts\activate 
     

run

    flask run --debug --host <ipaddress:port>                            

## Note

Please use developement requirements

To install from requirements

    pip install -r "./requirements/development.txt"

To add packages to developement config

    pip freeze > ".\requirements\development.txt"    

To perform migrations use the appropiate commands to perform migrations

    flask db init --directory src/migrations             
    flask db migrate --directory src/migrations -m "migration message"
    flask db upgrade --directory src/migrations
    flask db downgrade --directory src/migrations