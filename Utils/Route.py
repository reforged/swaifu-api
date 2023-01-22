def route(method: str = "get", url: str = None):
    def wrapper(fonction):
        fonction.method = method.upper()

        if url is not None:
            if url[0] != '/':
                fonction.append_url = url

            else:
                fonction.url = url

        return fonction
    return wrapper
