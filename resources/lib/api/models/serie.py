class Serie():
    def __init__(self, serie):
        self.serie = serie
        self.id = serie["id"]
        self.guid = serie["guid"]
        self.title = serie["title"]
        self.description = serie["description"]
        self.thumbnail = serie["thumbnail"]["url"]