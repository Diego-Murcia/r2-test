class Book:
    def __init__(self, id, title, subtitle, publish_date, editor, description, image, authors, categories):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.publish_date = publish_date
        self.editor = editor
        self.description = description
        self.image = image
        self.authors = authors
        self.categories = categories

    def __repr__(self):
        return f'Book({self.id}, {self.title}, {self.subtitle}, {self.publish_date}, {self.editor}, {self.description}, {self.image}, {self.authors}, {self.categories})'

    def to_dict(self):
        return {"id": self.id, "title": self.title, "subtitle": self.subtitle, "publish_date": self.publish_date, "editor": self.editor, "description": self.description, "image": self.image, "authors": self.authors, "categories": self.categories}
