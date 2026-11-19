class BasePage:
    path = "/"

    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto(self.path)
        return self
