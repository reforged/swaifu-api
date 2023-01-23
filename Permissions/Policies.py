from flask import request, make_response
from Erreurs.HttpErreurs import *
from BDD.Database import Database
from Utils.Dotenv import getenv
from datetime import datetime, timedelta
from BDD.BDD_PSQL.PsqlParsers import jsonToPsqlQuery
import jwt


def check_perm(db: Database, id: str, permissions: list):
    query = {
        "select": [
            ["permissions", "key"]
        ],
        "where": [
            ["users", "id", id, "and"]
        ],
        "from": {
            "tables": ["users", "permission_user", "permissions"],

            "cond": [
                [
                    ["users", "id"],
                    ["permission_user", "user_id"]
                ],
                [
                    ["permission_user", "permission_id"],
                    ["permissions", "id"]
                ]
            ]
        }
    }

    permission_labels = db.query(query)
    permission_labels = [valeur["label"] for valeur in permission_labels]

    print(f"Query res : {permission_labels}")

    if "admin" in permission_labels:
        return True

    for required_permission in permissions:
        if required_permission not in permission_labels:
            return False

    return True


def check_token(req, db: Database):
    if "Authorization" not in req.headers:
        return None

    token = req.headers["Authorization"][7:]

    try:
        decoded_token = jwt.decode(token, getenv("token_key"), algorithms=["HS256"])
    except:
        return None

    query = {
        "select": [
            ["api_tokens", "token"]
        ],
        "where": [
            ["api_tokens", "token", token, "and"]
        ],
        "from": {
            "tables": ["api_tokens"]
        }
    }

    query_result = db.query(query)

    if len(query_result) == 0:
        return None

    expires_at_datetime = query_result[0].get("expires_at", datetime.now() + timedelta(seconds=10))

    if expires_at_datetime < datetime.now():
        return None

    return decoded_token


def middleware(policies: list):
    def wrapper(fonction):
        def inner(*args, **kwargs):
            if "Authorization" not in request.headers:
                return make_response(non_authorise, 401, non_authorise)

            db: Database = kwargs["database"]

            if db is None:
                raise KeyError("Fonction nécessitant une connection à la BDD sans pouvoir.")

            decoded_token = check_token(request, db)

            if decoded_token is None:
                return make_response(token_invalide, 400, token_invalide)

            print(decoded_token)

            perm = check_perm(db, decoded_token["id"], policies)

            if not perm:
                return make_response(non_authorise, 403, non_authorise)

            return fonction(*args, **kwargs)

        inner.__name__ = fonction.__name__

        inner.info_fonction = {
            "co_argcount": getattr(getattr(fonction, "__code__"), "co_argcount"),
            "co_varnames": getattr(getattr(fonction, "__code__"), "co_varnames"),
            "__module__": getattr(fonction, "__module__")
        }

        return inner

    return wrapper
