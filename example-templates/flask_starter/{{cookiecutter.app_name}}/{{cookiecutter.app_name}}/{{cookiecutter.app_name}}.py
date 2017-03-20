import json

from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash, Response, jsonify

from core import app, project_relative_location


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/robots.txt')
def robots():
    return Response(open(project_relative_location('static/robots.txt')).read(), mimetype='text/plain')

