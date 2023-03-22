import Permissions.Policies as Policies

import BDD.Model as Model


@Policies.middleware(["user:post"])
def test(query_builder: Model.Model):
    return {"Message": "Good"}
