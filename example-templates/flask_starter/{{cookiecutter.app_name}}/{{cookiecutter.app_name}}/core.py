import os
import sys

from flask import Flask, url_for

reload(sys)
sys.setdefaultencoding('utf-8')


def project_relative_location(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)


def boolean(b):
    return b in ['True', 'T', 'true', 't', 'Yes', 'Y', 'yes', 'y', '1', True]


app = Flask(__name__)