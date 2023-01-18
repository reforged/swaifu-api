import json
import Permissions.Policies as Policies
import Erreurs.HttpErreurs as HttpErreurs
from flask import make_response, Response


def me(request, database) -> list | Response:
    token = Policies.check_token(request)

    if token is None:
        return make_response(HttpErreurs.non_authentifie, 400, HttpErreurs.non_authentifie)

    query = {
        "where": [
            ["users", "id", token["id"]]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(query)[0]
