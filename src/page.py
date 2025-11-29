class Page:
    def __init__(self, route: str, title: str, content: str, image_url: str = ""):
        self.route = route
        self.title = title
        self.content = content
        self.image_url = image_url

    def __eq__(self, other):
        if not isinstance(other, Page):
            return False
        return (self.route == other.route and
                self.title == other.title and
                self.content == other.content and
                self.image_url == other.image_url)
