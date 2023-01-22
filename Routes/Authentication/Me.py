import json
import Permissions.Policies as Policies
import Erreurs.HttpErreurs as HttpErreurs
from flask import make_response, Response


def me(request, database) -> list | Response:
    token = Policies.check_token(request, database)

    if token is None:
        return make_response(HttpErreurs.non_authentifie, 400, HttpErreurs.non_authentifie)

    query = {
        "select": [
            ["users", "firstname"],
            ["users", "email"],
            ["users", "lastname"],
            ["users", "created_at"],
            ["users", "updated_at"]
        ],
        "where": [
            ["users", "id", token["id"], "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(query)[0]
