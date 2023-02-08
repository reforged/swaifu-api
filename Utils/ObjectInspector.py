import Utils.Types as Types


def retrieveAttr(fonction, attribute: str, default=None):
    valeur_retour: Types.union_dss_n = default

    if hasattr(fonction, 'info_fonction'):
        valeur_retour = getattr(fonction, 'info_fonction').get(attribute) or default

    if valeur_retour == default:
        if hasattr(fonction, attribute):
            valeur_retour = getattr(fonction, attribute)

    return valeur_retour


def checkAttr(fonction, attribute: str):
    valeur_retour: bool = False

    if hasattr(fonction, 'info_fonction'):
        valeur_retour = getattr(fonction, 'info_fonction').get(attribute, False)

    if not valeur_retour:
        valeur_retour = hasattr(fonction, attribute)

    return valeur_retour
