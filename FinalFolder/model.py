from database import db
from datetime import datetime

# Define the Association Table for Many-to-Many between Recipe and Ingredient
recipe_ingredient = db.Table(
    'recipe_ingredient',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

# Define the Association Table for Many-to-Many between User and Recipe
user_likes = db.Table(
    'user_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('liked_on', db.DateTime, default=db.func.current_timestamp())
)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    # Many-to-Many relationship with Recipe through the 'user_likes' table
    liked_recipes = db.relationship('Recipe', secondary=user_likes, backref='liked_by', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

# Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # Many-to-Many Relationship with Ingredient
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredient, backref='recipes')

    # Many-to-One Relationship with Category
    category = db.relationship('Category', backref=db.backref('recipes', lazy=True))

    def __repr__(self):
        return f'<Recipe {self.title}>'

    @classmethod
    def get_recipes_by_category(cls, category_name):
        return cls.query.join(Category).filter(Category.name == category_name).all()

# Ingredient Model
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    quantity = db.Column(db.String(50), nullable=True)  # Optional for flexibility

    def __repr__(self):
        return f'<Ingredient {self.name}>'

# Category Model
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.name}'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    highlighted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Message from {self.name}>'
