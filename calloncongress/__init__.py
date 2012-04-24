import datetime
import pymongo

from flask import Flask, g
from calloncongress.web import web
from calloncongress.voice import voice
# from calloncongress.sms import sms


app = Flask(__name__)
app.register_blueprint(web)
app.register_blueprint(voice, url_prefix='/voice')
# app.register_blueprint(sms, url_prefix='/sms')


@app.before_request
def before_request():
    """
    Sets up request context by setting current request time (UTC),
    creating MongoDB connection and reference to collection.
    """
    g.now = datetime.datetime.utcnow()
    g.conn = pymongo.Connection()
    g.db = g.conn.capitolphone


@app.after_request
def after_request(response):
    """
    Saves the call object from the request context if one exists.
    """
    if hasattr(g, 'call') and g.call is not None:
        g.db.calls.save(g.call)
    return response


@app.teardown_request
def teardown_request(exception):
    """
    Disconnects from the MongoDB instance.
    """
    g.conn.disconnect()
