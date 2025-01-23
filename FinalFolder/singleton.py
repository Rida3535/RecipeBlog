from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Recipe  # Assuming Recipe model is already defined

class RecipeDatabase:
    _instance = None
    _engine = None
    _Session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RecipeDatabase, cls).__new__(cls)
            
            # Initialize database connection and session
            cls._engine = create_engine('sqlite:///recipes.db', echo=True)  # SQLite URI
            cls._Session = sessionmaker(bind=cls._engine)
            cls._instance.session = cls._Session()
        
        return cls._instance

    def add_recipe(self, recipe):
        self.session.add(recipe)
        self.session.commit()

    def get_all_recipes(self):
        return self.session.query(Recipe).all()

    def get_recipes_by_category(self, category):
        return self.session.query(Recipe).filter_by(category=category).all()
