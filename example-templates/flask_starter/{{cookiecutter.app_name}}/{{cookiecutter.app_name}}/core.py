import os
import sys

from flask import Flask, url_for

reload(sys)
sys.setdefaultencoding('utf-8')


def project_relative_location(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)


app = Flask(__name__)