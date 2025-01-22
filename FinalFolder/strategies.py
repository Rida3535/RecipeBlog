class SearchStrategy:
    def search(self, recipes, query):
        raise NotImplementedError("Search method must be implemented.")

class SimpleSearchStrategy(SearchStrategy):
    def search(self, recipes, query):
        return [recipe for recipe in recipes if query.lower() in recipe.title.lower()]

class AdvancedSearchStrategy(SearchStrategy):
    def search(self, recipes, query, filter_by=None):
        # Example: Extend filtering logic here
        filtered_recipes = [
            recipe for recipe in recipes if query.lower() in recipe.title.lower()
        ]
        if filter_by:
            filtered_recipes = [
                recipe for recipe in filtered_recipes if filter_by(recipe)
            ]
        return filtered_recipes
