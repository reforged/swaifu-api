from Link import Link
from ManyToMany import ManyToMany
import datetime


def getTime():
    return datetime.datetime.now().astimezone()


class Table:
    """
    Classe mère pour tout les schémas de tables, et fourni les fonctionnalités communes et nécessaire
    """
    table_name: str = None
    primary_key: str = "id"

    def __init__(self, model, **kwargs):
        """
        Prends un modèle de classe pour pouvoir construire des requêtes, et éventuellement des paramètres nommés,
        servant à remplir le schéma d'information
        """
        self.model_class = model

        for key in self.__annotations__:
            if self.__dict__.get(key) is not None:
                self.__dict__[key] = None

        if self.table_name is None:
            # Si le nom de la table est précisé il est pris, sinon il s'agit du nom de la classe en minuscule
            # (convention)
            self.table_name = self.__class__.__name__.lower()

        for key in self.__annotations__:
            # __annotations__ correspond aux déclarations de types effectués dans la classe, et donc les seuls paramètre
            # Nous intéressant
            self.__setattr__(key, kwargs.get(key))

    def __repr__(self):
        """
        Permet de fournir une représentation de l'objet

        Exclu les valeurs None
        """

        # Le nom de la table ne correspond par forcément au nom de la classe
        returnStr = type(self).__name__ + "("

        for key in self.__annotations__:
            if self.__dict__[key] is not None:
                returnStr += f"{key}='{str(self.__dict__[key])}', "

        # Pour éventuellement enlever le `, ` de trop à la fin
        if len(self.__dict__) > 0:
            returnStr = returnStr[:-2]

        returnStr += ")"

        return returnStr

    def export(self, convert: bool = False):
        """
        Exporte la classe actuelle sous forme de dictionnaire, pour une utilisation éventuelle ou pour le sérialiser
        """
        return_values = {}

        for key in self.__annotations__:
            # Pour chaque valeur déclarée dans le schéma
            if self.__dict__.get(key) is not None:
                # S'il existe une valeur
                if issubclass(type(self.__annotations__[key]), Link):
                    # S'il s'agit d'une déclaration d'une relation, alors on appelle récursivement la méthode
                    if type(self.__dict__[key]) == list:
                        return_values[key] = [row.export(convert) for row in self.__dict__[key]]
                    else:
                        return_values[key] = self.__dict__[key].export(convert)
                else:
                    # Si c'est une valeur, tel que str, alors on ajoute tel que
                    if convert:
                        if type(self.__dict__[key]) not in [str, int, float, bool]:
                            return_values[key] = str(self.__dict__[key])
                        else:
                            return_values[key] = self.__dict__[key]
                    else:
                        return_values[key] = self.__dict__[key]

        return return_values

    def load(self, field, cond=None):
        """
        Fonction s'occupant du chargement sur l'objet d'une variable, en fonction d'une relation déclarée

        :param field: Le nom de la variable déclarée à charger
        :param cond: Eventuellement une requête déjà construite, par exemple pour sélectionner certaines colonnes
        """

        annotations = self.__annotations__

        for key in annotations:
            # Pour chaque valeur déclarée
            if issubclass(type(annotations[key]), Link):
                # S'il s'agit bien d'un lien

                if key.lower() == field.lower():
                    # Et qu'il s'agit de la bonne variable, on charge
                    link = annotations[key]

                    join_on = self.primary_key
                    join_from = "id"

                    if link.__dict__.get("primary_key") is not None:
                        # Par défaut la clé primaire est `id`, mais éventuellement la table sur laquelle nous effectuons
                        # Le chargement peut avoir une clé primaire différente
                        join_from = link.__dict__.get("primary_key")
                        # Chargement de la valeur de l'id que nous souhaitons (where)
                        wanted_value = self.__dict__.get(join_from)

                        if wanted_value is None:
                            raise ValueError("Valeur de la clé primaire manquante pour la requête")

                    # Dans le cas d'une relation `ManyToMany` la vie n'est pas aussi simple
                    # Puisque nous passons par une table pivot, et remplaçons la valeur de la variable par ce qui est
                    # Déclaré directement, sans trace de la table pivot, d'où la perte éventuelle d'informations
                    if type(link) is not ManyToMany:
                        # Eventuellement la clé de l'autre table n'est pas la clé primaire, pareil pour nous
                        if link.__dict__.get("join_from") is not None:
                            join_from = link.join_from
                        if link.__dict__.get("join_on") is not None:
                            join_on = link.join_on

                    # On revérifie la valeur souhaitée puisque join_from a pu changer
                    wanted_value = self.__dict__.get(join_from)

                    # Si aucun modèle est donnée, nous créons un de base prenant tout
                    if cond is not None:
                        query = link.getQuery(cond, join_on, wanted_value, self.table_name)
                    else:
                        # Sinon on construit dessus, en précisant que nous souhaitons tout dans la table pivot
                        query_model = self.model_class.copy().select(f"{link.table_name}.*")
                        # Puis nous demandons à la relation de créer le reste de la requête pour nous
                        query = link.getQuery(query_model, join_on, wanted_value, self.table_name)

                    # Avant de l'exécuter, et la filter (eg : HasOne -> spécial)
                    query_res = link.filter(query.execute(False))

                    # Pour enfin l'ajotuer comme attribut à la classe appelante
                    setattr(self, key, query_res)

        return self

