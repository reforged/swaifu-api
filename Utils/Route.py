def route(method: str = "get", url: str = None):
    """
    Fonction permettant de contrôler l'url d'une fonction, indépendamment de son nom et placement dans la hiérarchie.

    :param method:
    :param url: Url de la fonction, s'ajoute à l'url de groupe si ne commence pas par `/`
    """
    def wrapper(fonction):
        """
        Fonction modifiant les attributs d'une fonction pour stocker la volonté d'url et de méthode d'accès.
        """
        fonction.method = method.upper()

        if url is not None:
            if url[0] != '/':
                fonction.append_url = url

            else:
                fonction.url = url

        return fonction
    return wrapper
