from model import db, Recipe, User, Category

class RecipeRepository:
    def get_all_recipes(self):
        return Recipe.query.all()

    def get_recipe_by_id(self, recipe_id):
        return db.session.get(Recipe, recipe_id)

    def add_recipe(self, recipe):
        db.session.add(recipe)
        db.session.commit()

    def delete_recipe(self, recipe_id):
        recipe = db.session.get(Recipe, recipe_id)
        if recipe:
            db.session.delete(recipe)
            db.session.commit()    

class UserRepository:
    def get_user_by_id(self, user_id):
        return db.session.get(User, user_id)

    def get_user_by_email(self, email):
        return db.session.query(User).filter_by(email=email.lower()).first()

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()

    def like_recipe(self, user_id, recipe_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        recipe = db.session.get(Recipe, recipe_id)
        if recipe and recipe not in user.liked_recipes:
            user.liked_recipes.append(recipe)
            db.session.commit()
            return True
        return False

    def get_liked_recipes(self, user_id):
        user = self.get_user_by_id(user_id) 
        if user:
            return user.liked_recipes  
        return [] 
    def unlike_recipe(self, user_id, recipe_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        recipe = db.session.get(Recipe, recipe_id)
        if recipe and recipe in user.liked_recipes:
            user.liked_recipes.remove(recipe)
            db.session.commit()
            return True
        return False

# Category Repository
class CategoryRepository:
    @staticmethod
    def get_all_categories():
        return Category.query.all()

    def get_recipes_by_category(self, category_name):
        return db.session.query(Recipe).filter(Recipe.category.has(name=category_name)).all()

