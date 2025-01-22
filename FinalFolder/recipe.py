from abstract import Recipe

# Concrete Recipe Class
class SimpleRecipe(Recipe):
    def __init__(self, title, description, image, category):
        self._title = title
        self._description = description
        self._image = image
        self._category = category

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_image(self):
        return self._image

    @property
    def category(self):
        return self._category
