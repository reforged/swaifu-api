import BDD.Model as Model


def getAllRoles(query_builder: Model.Model):
    """
    Gère la route .../roles - Méthode GET

    Permet à un utilisateur de récupérer tous les rôles.

    :param query_builder: Objet Model
    """

    info_wanted = ["users.id", "users.email", "users.numero", "users.firstname", "users.lastname", "users.created_at", "users.updated_at"]

    # Pour chaque rôle, on charge les utilisateurs l'ayant
    # ET POUR LA DERNIERE FOIS ON NE PREND PAS LE MOT DE PASSE
    res = query_builder.table("roles").load("users", query_builder.select(*info_wanted))

    for row in res:
        # On charge également les permissions associés, séparemment de users car le chargement horizontal n'est pas
        # Possible
        row.load("permissions")

    return [row.export() for row in res]
