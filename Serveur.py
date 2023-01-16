import flask
import json
import os

import Utils.RoutesImporter as RoutesImporter

api_url = "/api/v1"
RoutesImporter.current_dir = os.path.dirname(__file__)

App = flask.Flask(__name__)

RoutesImporter.import_route("Routes", os.path.dirname(__file__), "/", App, os.path.basename(__file__))

App.run()
