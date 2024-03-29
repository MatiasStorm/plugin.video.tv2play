from .node import Node

class Serie(Node):
    def __init__(self, serie):
        self.serie = serie
        id = serie["guid"]
        title = serie["title"]
        plot = serie["description"]
        thumbnail = serie.get("thumbnail", None)
        thumb = None
        if thumbnail is not None:
            thumb = thumbnail.get("url", None)
        Node.__init__(self, id=id, title=title, plot=plot, thumb=thumb)

    def has_seasons(self):
        return len(self.serie["seasons"]["nodes"]) > 0

