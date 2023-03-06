import os

with open(r"C:\Users\ospat\PycharmProjects\Api\.env", "r") as file:
    result = (file.read()).split("\n")

store = {key: value for key, value in [line.split("=") for line in result]}


def getenv(key):
    return store.get(key)
