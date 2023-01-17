def route(method: str = "get", url: str = None):
    def wrapper(fonction):
        fonction.method = method.upper()

        if url is not None:
            fonction.url = url

        return fonction
    return wrapper
