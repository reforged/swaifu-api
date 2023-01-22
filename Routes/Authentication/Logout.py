from flask import make_response
import Permissions.Policies as Policies
import Erreurs.HttpErreurs as HttpErreurs
from Utils.Route import route


@route(method="delete")
def logout(database, request):
    token = None

    if "Authorization" in request.headers:
        token = request.headers["Authorization"][7:]

    if token is None:
        return make_response(HttpErreurs.non_authentifie, 400, HttpErreurs.non_authentifie)

    remove_token_query = {
        "table": "api_tokens",
        "action": "delete",
        "valeurs": [
            ["token",  "Bearer " + token]
        ]
    }

    database.execute(remove_token_query)
    database.commit()

    return {"token": token}
