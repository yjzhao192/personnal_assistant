import backend.settings


def proxy():
    if backend.settings.USE_PROXY:
        return {}
    else:
        return {}
