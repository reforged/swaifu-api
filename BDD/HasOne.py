from BDD.Link import Link


class HasOne(Link):
    """
    Classe représentant un lien de type `ManyToOne` et stocke les informations relevantes
    """
    table_name: str
    join_from: str
    join_on: str

    def __init__(self, table_name: str, join_from: str, join_on: str = None):
        if table_name is None or join_from is None:
            raise ValueError("Paramètres manquants à HasMany")

        self.table_name = table_name
        self.join_from = join_from

        if join_on is not None:
            self.join_on = join_on

    def getQuery(self, model, join_on_name: str, join_on_value: str, caller_table_name: str):
        """
        Effectue la requête pour obtenir la donnée à laquelle le champ est lié (Ne fait que préparer la requête, et ne
        l'exécute pas)
        """

        query = model.table(self.table_name)

        # Dans le cas où `join_on` est défini, qui correspond à la clé étrangère de la table côté One, on l'utilise
        # (Au lieu de la valeur par défaut qui est `id`
        if self.__dict__.get("join_on") is not None:
            join_on_name = self.join_on

        return query.where(join_on_name, join_on_value)

    def filter(self, query: list):
        # Sachant que pour une relation ManyToOne nous n'aurons toujours qu'au plus qu'un seul Objet correspondant,
        # Il n'y a aucun intérêt, voir même un contre-intuitif de renvoyer une liste, nous renvoyant donc directement
        # L'objet
        if len(query) > 0:
            return query[0]
        return
