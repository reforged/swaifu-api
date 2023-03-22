class BDDNonPriseEnCharge(Exception):
    """
    Exception générique pour l'initialisation du serveur, si jamais une BDD non prise en charge est demandée
    """
    def __init__(self, message):
        super().__init__(message)
