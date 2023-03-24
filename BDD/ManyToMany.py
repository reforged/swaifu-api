from BDD.Link import Link
from BDD.Pivot import Pivot


class ManyToMany(Link):
    """
    Classe représentant un lien de type `ManyToMany` et stocke les informations relevantes pour
    en raison du type de lien, une table pivot doit être utilisé, et par simplicité, cette classe renvoie une liste
    des objets désirés comme si la table pivots n'existais pas.

    Il y a éventuellement une perte de champs.
    """

    table_name: str
    table_pivot: Pivot

    def __init__(self, table_name: str, table_pivot):
        """
        Prends le nom de la table souhaité et l'objet Pivot représentant la table pivot
        """
        self.table_name = table_name
        self.table_pivot = table_pivot()

    def getQuery(self, model, primary_key_name, primary_key_value, caller_table_name):
        self_table_name = self.table_name

        table_pivot = self.table_pivot
        table_pivot_name = table_pivot.table_name
        table_pivot_annot = table_pivot.__annotations__

        table_pivot_pk = table_pivot_annot.get(self_table_name).join_from

        caller_table_pk = table_pivot_annot.get(caller_table_name).join_from

        return model.table(self.table_name).where(f"{table_pivot_name}.{caller_table_pk}", primary_key_value).join(table_pivot_name, f"{self_table_name}.{primary_key_name}", f"{table_pivot_name}.{table_pivot_pk}")
