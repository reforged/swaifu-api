import BDD.Database as Database


def getPasswordByEmail(database: Database.Database, email: str) -> list[dict[str, str]]:
    password_request = {
        "where": [
            ["users", "email", email, "and"]
        ],
        "from": {
            "tables": ["users"]
        }
    }

    return database.query(password_request)
