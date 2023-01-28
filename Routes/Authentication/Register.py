import jwt
from Utils.Dotenv import getenv
from BDD.Database import Database
from flask import Request, make_response
from Erreurs.HttpErreurs import requete_malforme, creation_impossible
from Utils.Route import route
import datetime
from Permissions.Policies import middleware
import Utils.HandleUser as HandleUser
import Utils.HandleToken as HandleToken


# @middleware(["post:user"])
@route(method="post")
def register(database: Database, request: Request):
    data = request.get_json()

    firstname = data.get("firstname", None)
    lastname = data.get("lastname", None)
    email = data.get("email", None)

    for object in ["firstname", "lastname", "email", "password"]:
        if data.get(object, None) is None:
            return make_response(requete_malforme, 400, requete_malforme)

    if len(database.query(HandleUser.getUserByEmail(database, email))) != 0:
        return make_response(creation_impossible, 409, creation_impossible)

    user_uuid = HandleUser.addUser(database, data)

    token = jwt.encode({'id': user_uuid}, getenv("token_key"), algorithm="HS256")

    HandleToken.addToken(database, token, user_uuid)

    return_data = {'token': "Bearer " + token, 'user': {
        'id': user_uuid,
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'created_at': str(datetime.datetime.now().astimezone()),
        'updated_at': str(datetime.datetime.now().astimezone())
    }
                   }

    return return_data
