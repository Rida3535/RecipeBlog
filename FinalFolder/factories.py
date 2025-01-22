from recipe import SimpleRecipe

# Recipe Factory Design Pattern
class RecipeFactory:
    @staticmethod
    def create_recipe(title, description, image, category):
        return SimpleRecipe(title, description, image, category)