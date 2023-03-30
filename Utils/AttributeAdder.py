def add_attributes(dict_arguments: dict[str, any]):
    """
    Fonction fournissant des paramètres à la fonction décorée en fonction des paramètres déclarés.

    :param dict_arguments: Liste des paramètres potentiellement fournissables aux fonctions
    """
    def wrapper(fonction):
        """
        Fonction récupérant et stockant les paramètres demandés pour pouvoir les fournir lors des appels de la fonction.

        :param fonction: Fonction à qui fournir les paramètres à
        """
        co_varnames = getattr(getattr(fonction, "__code__"), "co_varnames")

        if hasattr(fonction, "info_fonction"):
            co_varnames = (getattr(fonction, "info_fonction")).get("co_varnames", co_varnames)

        arguments_demandes = {key: dict_arguments[key] for key in dict_arguments if key in co_varnames}

        def inner(*args, **kwargs):
            return fonction(*args, **kwargs, **arguments_demandes)

        inner.__name__ = fonction.__name__

        return inner

    return wrapper