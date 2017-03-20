import argh
import logging
import coloredlogs


@argh.arg('l', type=int)
def func1(l):
    pass


parser = argh.ArghParser()
parser.add_commands([func1])

if __name__ == '__main__':
    logging_format = '[%(asctime)s] %(levelname)s: %(message)s'
    coloredlogs.install(level='INFO', logger=logging.getLogger(), fmt=logging_format)

    parser.dispatch()
