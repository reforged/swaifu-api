from dataclasses import dataclass


def decorator(object):
    """
    Permet simplement de transformer en dataclass une table, créé pour simplifier légèrement la syntaxe et fixer des
    paramètres (ôter le contrôle de l'écrivain)
    """
    return dataclass(object, init=False, repr=False)
