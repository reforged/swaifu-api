class Link:
    """
    Classe mère pour toutes les relations entre table
    """

    table_name: str

    def getQuery(self, model, primary_key_name, primary_key_value, caller_table_name):
        """
        Effectue la requête pour obtenir la donnée à laquelle le champ est lié (Ne fait que préparer la requête, et ne
        l'exécute pas)
        """
        pass

    def filter(self, query: list):
        """
        Permet d'éventuellement filtrer la donnée en fonction de la relation
        """
        return query
