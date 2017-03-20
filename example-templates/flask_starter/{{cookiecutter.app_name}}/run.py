import argh
import logging

from {{cookiecutter.app_name}} import core
from {{cookiecutter.app_name}}.{{cookiecutter.app_name}} import app


@argh.arg('--host', type=str)
@argh.arg('--port', type=int)
@argh.arg('--debug', type=str)
def deploy(host='localhost', port='2700', debug='True'):
    app.debug = core.boolean(debug)
    app.run(host=host, port=port)


parser = argh.ArghParser()
parser.add_commands([deploy])


if __name__ == '__main__':
    logging_format = '[%(asctime)s] %(levelname)s: %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)

    parser.dispatch()
