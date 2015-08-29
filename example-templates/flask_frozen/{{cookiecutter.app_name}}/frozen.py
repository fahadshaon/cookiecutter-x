import os

from flask.ext.frozen import Freezer
from {{cookiecutter.app_name}}.{{cookiecutter.app_name}} import app

build_dir = os.path.realpath(os.path.join('data', 'build'))
app.config['FREEZER_DESTINATION'] = build_dir

freezer = Freezer(app, with_static_files=False, log_url_for=True)

if __name__ == '__main__':
    print 'Writing generated site to {}'.format(app.config['FREEZER_DESTINATION'])
    freezer.freeze()
