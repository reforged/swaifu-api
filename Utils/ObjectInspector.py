def retrieveAttr(fonction, attribute, default=None):
    valeur_retour = default

    if hasattr(fonction, 'info_fonction'):
        valeur_retour = getattr(fonction, 'info_fonction').get(attribute) or default

    if valeur_retour == default:
        if hasattr(fonction, attribute):
            valeur_retour = getattr(fonction, attribute)

    return valeur_retour


def checkAttr(fonction, attribute):
    valeur_retour = False

    if hasattr(fonction, 'info_fonction'):
        valeur_retour = getattr(fonction, 'info_fonction').get(attribute, False)

    if not valeur_retour:
        valeur_retour = hasattr(fonction, attribute)

    return valeur_retour
