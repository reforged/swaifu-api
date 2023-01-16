import flask
import json

app = flask.Flask(__name__)


@app.route('/')
def main():
    return json.dumps({"resultat": "Succès"})


app.run()
