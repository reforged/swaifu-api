from BDD.Link import Link


class HasMany(Link):
    """
    Classe représentant un lien de type `OneToMany` et stocke les informations relevantes
    """
    table_name: str
    join_on: str
    join_from: str

    def __init__(self, table_name: str, join_on: str, join_from: str = None):
        if table_name is None or join_on is None:
            raise ValueError("Paramètres manquants à HasMany")

        self.table_name = table_name
        self.join_on = join_on

        if join_from is not None:
            self.join_from = join_from

    def getQuery(self, model, join_from_name: str, join_from_value: str, caller_table_name: str):
        """
        Effectue la requête pour obtenir la donnée à laquelle le champ est lié (Ne fait que préparer la requête, et ne
        l'exécute pas)
        """

        return model.table(self.table_name).where(self.join_on, join_from_value)
