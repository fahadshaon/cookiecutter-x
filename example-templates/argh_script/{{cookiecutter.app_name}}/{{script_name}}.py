import argh
import logging


@argh.arg('l', type=int)
def func1(l):
    pass


parser = argh.ArghParser()
parser.add_commands([func1, func2])

if __name__ == '__main__':
    logging_format = '[%(asctime)s] %(levelname)s: %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)

    requests_logger = logging.getLogger("requests.packages.urllib3.connectionpool")
    requests_logger.setLevel(logging.WARN)

    parser.dispatch()
