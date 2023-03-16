import Utils.Types as Types


def retrieveAttr(fonction, attribute: str, default=None):
    """
    Fonction permettant de récupérer un attribut d'une fonction, adaptée pour prendre en compte une fonction ayant comme
    attribut `info_fonction`, signe que celle-ci a été décorée.

    :param fonction: Fonction concernée
    :param attribute: Attribut à rechercher
    :param default: Valeur par défaut, si l'attribut n'est pas trouvé
    """

    valeur_retour: Types.union_dss_n = default

    if hasattr(fonction, 'info_fonction'):
        valeur_retour = getattr(fonction, 'info_fonction').get(attribute) or default

    if valeur_retour == default:
        if hasattr(fonction, attribute):
            valeur_retour = getattr(fonction, attribute)

    return valeur_retour


def checkAttr(fonction, attribute: str):
    """
    Fonction permettant de vérifier si une fonction possède un attribut ou non, adaptée pour prendre en compte une
    fonction ayant comme attribut `info_fonction`, signe que celle-ci a été décorée.
    """
    valeur_retour: bool = False

    if hasattr(fonction, 'info_fonction'):
        valeur_retour = getattr(fonction, 'info_fonction').get(attribute, False)

    if not valeur_retour:
        valeur_retour = hasattr(fonction, attribute)

    return valeur_retour
