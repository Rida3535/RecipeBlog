from model import db, Recipe, User, Category

class RecipeRepository:
    def get_all_recipes(self):
        return Recipe.query.all()

    def get_recipe_by_id(self, recipe_id):
        return Recipe.query.get(recipe_id)

    def add_recipe(self, recipe):
        db.session.add(recipe)
        db.session.commit()

    def delete_recipe(self, recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()    

class UserRepository:
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_user_by_email(self, email):
        return db.session.query(User).filter_by(email=email.lower()).first()

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()

    def like_recipe(self, user_id, recipe_id):
        user = self.get_user_by_id(user_id)  
        recipe = Recipe.query.get(recipe_id)  
        if user and recipe:
            # Check if the user has already liked the recipe (using the `user_likes` association table)
            if recipe in user.liked_recipes:
                return False  # User has already liked this recipe, so no action is performed
        
            # Add the recipe to the user's liked_recipes
            user.liked_recipes.append(recipe)
            db.session.commit()  
            return True  # Successfully liked the recipe
        return False  # User or recipe not found

    def get_liked_recipes(self, user_id):
        user = self.get_user_by_id(user_id)  # Get user by ID
        if user:
            return user.liked_recipes  # Return the list of liked recipes
        return []  # Return an empty list if user not found

# Category Repository
class CategoryRepository:
    @staticmethod
    def get_all_categories():
        return Category.query.all()

    def get_recipes_by_category(self, category_name):
        return db.session.query(Recipe).filter(Recipe.category.has(name=category_name)).all()
