def route(method: str = "GET", url: str = None):
    """
    Fonction permettant de contrôler l'url d'une fonction, indépendamment de son nom et placement dans la hiérarchie.
    Ainsi que la méthode qu'elle offre (GET / POST / PUT / DELETE)

    :param method: Méthode que la fonction propose (un seul)
    :param url: Url de la fonction, s'ajoute à l'url de groupe si ne commence pas par `/`
    """
    def wrapper(fonction):
        """
        Fonction modifiant les attributs d'une fonction pour stocker la volonté d'url et de méthode d'accès.
        """
        if hasattr(fonction, "info_fonction"):
            fonction.info_fonction["method"] = method.upper()
        else:
            fonction.info_fonction = {"method": method.upper()}

        if url is not None:
            if url[0] != '/':
                fonction.append_url = url

            else:
                fonction.url = url

        return fonction
    return wrapper
