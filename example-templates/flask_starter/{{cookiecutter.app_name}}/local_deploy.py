# To deploy first need to install dependencies, preferably with virtualenv -
#
#    . venv/bin/activate
#    pip install -r requirements.txt
#
# Then run local_deploy.py script -
#
#    python local_deploy.py

import argparse
import logging

## LOCAL_ENV_IMPORT ##
from {{cookiecutter.app_name}}.{{cookiecutter.app_name}} import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='{{cookiecutter.app_description}}')

    parser.add_argument('--host', default='127.0.0.1', help='Host bind location')
    parser.add_argument('--port', default=2700, type=int, help='Port')
    parser.add_argument('--debug', default="True", type=str, help='Enable of disable debug, default True')

    args = parser.parse_args()
    args.debug = True if args.debug in ['True', 'T', 'true', 't', 'Yes', 'Y', 'yes', 'y', '1'] else False

    # Logging
    logging_format = '[%(asctime)s] %(levelname)s: %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)

    # Starting the application
    app.debug = args.debug
    app.run(host=args.host, port=args.port)
