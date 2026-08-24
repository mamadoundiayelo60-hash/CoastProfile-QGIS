def classFactory(iface):
    from .plugin import CoastProfilePlugin
    return CoastProfilePlugin(iface)
