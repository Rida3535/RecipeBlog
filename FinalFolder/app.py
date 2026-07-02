from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from model import Recipe, User, Category, Ingredient, ContactMessage
from repositories import RecipeRepository, UserRepository, CategoryRepository
from database import db
from flask_migrate import Migrate
import os
from werkzeug.utils import secure_filename
import re

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Repositories
recipe_repository = RecipeRepository()
user_repository = UserRepository()
category_repository = CategoryRepository()

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home Page Route - Display all recipes
@app.route('/')
def home():
    liked_recipe_id = []
    if 'user_id' in session:
        user = user_repository.get_user_by_id(session['user_id'])
        if user:
            liked_recipe_id = [recipe.id for recipe in user.liked_recipes]
        else:
            session.pop('user_id', None)

    recipes = recipe_repository.get_all_recipes()  # Get all recipes
    return render_template('index.html', recipes=recipes, liked_recipe_id=liked_recipe_id)


# Recipe List Route (for listing all recipes or filtering by category)
@app.route('/recipe', defaults={'category': None})
@app.route('/recipe/<string:category>')
def recipe(category):
    liked_recipe_id = []
    if 'user_id' in session:
        user = user_repository.get_user_by_id(session['user_id'])
        if user:
            liked_recipe_id = [recipe.id for recipe in user.liked_recipes]
        else:
            session.pop('user_id', None)

    if category:
        recipes = Recipe.query.join(Category).filter(Category.name == category).all()
    else:
        recipes = Recipe.query.all()  # Get all recipes without adding any specific text
  
    return render_template('recipe.html', recipes=recipes, category=category, liked_recipe_id=liked_recipe_id)

# Recipe Detail Route (specific to a single recipe)
@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_details(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)  # Retrieve the recipe by ID
    return render_template('recipe_details.html',recipe=recipe)

# About Route
@app.route('/about')
def about():
    return render_template('about.html')  

# User Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email'].lower()
        password = request.form['password']
        
        # Check if user already exists
        if user_repository.get_user_by_email(email):
            flash("Email already registered", "danger")
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
               
        # For admin registration, set `is_admin=True`
        is_admin = email == 'admin@example.com'  # For example, manually set the admin
        user = User(username=username, email=email, password=hashed_password, is_admin=is_admin)
        user_repository.add_user(user)

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = user_repository.get_user_by_email(email.lower())
        
        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                return redirect(url_for('home'))
            else:
                flash('Login failed! Incorrect password.', 'danger')
        else:
            flash('Login failed! No user found with that email.', 'danger')
    
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

# Like a Recipe Route
@app.route('/like_recipe/<int:recipe_id>', methods=['POST'])
def like_recipe(recipe_id):
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Please log in to like recipes."})

    user = user_repository.get_user_by_id(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return jsonify({"success": False, "message": "Please log in to like recipes."})

    recipe = recipe_repository.get_recipe_by_id(recipe_id)

    if not recipe:
        return jsonify({"success": False, "message": "Recipe not found."})

    # Check if the recipe is already liked by the user
    if recipe not in user.liked_recipes:
        user.liked_recipes.append(recipe)
        db.session.commit()
        return jsonify({"success": True, "message": f'You liked the recipe "{recipe.title}".'})
    else:
        return jsonify({"success": False, "message": f'You have already liked the recipe "{recipe.title}".'})


@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    ingredient_name = request.form.get('ingredient_name')
    
    if not ingredient_name:
        return "Missing ingredient name", 400
    
    ingredient = Ingredient(name=ingredient_name)
    db.session.add(ingredient)
    db.session.commit()

    return f"Ingredient {ingredient.name} added successfully!"

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add Recipe Route
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user_id' not in session:
        flash('Please login to add recipes.', 'warning')
        return redirect(url_for('login'))
    
    recipe=None
    user = user_repository.get_user_by_id(session['user_id'])
    if not user:
        session.pop('user_id', None)
        flash('Please login to add recipes.', 'warning')
        return redirect(url_for('login'))

    categories = category_repository.get_all_categories()

    if not user.is_admin:
        flash('Only the admin can add recipes.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        ingredients_str = request.form['ingredients']
        instructions = request.form['instructions']
        category_id = request.form['category']
        category = db.session.get(Category, category_id)

        if not category:
            flash('Invalid category selected.', 'danger')
            return redirect(url_for('add_recipe'))

        # Handle file upload
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = 'default_image.jpg'  

        # Create the Recipe object
        recipe = Recipe(
            title=title,
            description=description,
            instructions=instructions,
            category_id=category.id,
            image=filename 
        )

        # Add ingredients
        ingredients_list = ingredients_str.split(',')
        for ingredient in ingredients_list:
            name_quantity = ingredient.strip().split(':')
            if len(name_quantity) == 2:
                name = name_quantity[0].strip()
                quantity = name_quantity[1].strip()
                ingredient_instance = Ingredient.query.filter_by(name=name).first()

                if not ingredient_instance:
                    ingredient_instance = Ingredient(name=name, quantity=quantity)
                    db.session.add(ingredient_instance)
                
                recipe.ingredients.append(ingredient_instance)

        # Save recipe
        db.session.add(recipe)
        db.session.commit()

        flash('Recipe added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_recipe.html', recipe=recipe, categories=categories)

# Edit Recipe Route
@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = user_repository.get_user_by_id(session['user_id'])
    if not user or not user.is_admin:
        if not user:
            session.pop('user_id', None)
        return redirect(url_for('home'))

    recipe = recipe_repository.get_recipe_by_id(recipe_id)
    if not recipe:
        return redirect(url_for('admin_dashboard'))

    categories = category_repository.get_all_categories()

    if request.method == 'POST':
        # Update the recipe details
        recipe.title = request.form['title']
        recipe.description = request.form['description']
        recipe.instructions = request.form['instructions']
        recipe.category_id = request.form['category']

        # Update ingredients
        ingredients_str = request.form['ingredients']
        recipe.ingredients.clear()
        ingredients_list = ingredients_str.split(',')
        for ingredient in ingredients_list:
            name_quantity = ingredient.strip().split(':')
            if len(name_quantity) == 2:
                name = name_quantity[0].strip()
                quantity = name_quantity[1].strip()

                ingredient_instance = Ingredient.query.filter_by(name=name).first()
                if not ingredient_instance:
                    ingredient_instance = Ingredient(name=name, quantity=quantity)
                    db.session.add(ingredient_instance)
                else:
                    ingredient_instance.quantity = quantity

                recipe.ingredients.append(ingredient_instance)

        # Update image
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename != '':
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(image_path)
                recipe.image = filename

        # Save changes
        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_recipe.html', recipe=recipe, categories=categories)

# User Profile 
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = user_repository.get_user_by_id(session['user_id'])  

    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    
    liked_recipes = user_repository.get_liked_recipes(session['user_id'])

    return render_template(
        'profile.html', 
        username=user.username, 
        email=user.email,
        liked_recipes=liked_recipes
    )

#Unlike Recipe Route
@app.route('/unlike_recipe/<int:recipe_id>', methods=['POST'])
def unlike_recipe(recipe_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user_repository.unlike_recipe(session['user_id'], recipe_id)
    return redirect(url_for('profile'))

# Contact Page Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        # Validate fields
        if not all([name, email, message]):
            flash("All fields are required!", "danger")
            return redirect(url_for('contact'))

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            flash("Invalid email format!", "warning")
            return redirect(url_for('contact'))

        if 'user_id' in session:
            user = user_repository.get_user_by_id(session['user_id'])
            if user and (user.username != name or user.email != email):
                flash("The provided name or email does not match your account!", "danger")
                return redirect(url_for('contact'))

        # Save the contact message
        new_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html')

# Admin Message Route
@app.route('/admin/messages')
def admin_messages():
    if 'user_id' not in session or not session.get('is_admin', False):
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('home'))

    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin_messages.html', messages=messages)

# Delete message Route
@app.route('/delete_message/<int:message_id>')
def delete_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin_messages'))

# Highlight Message Route
@app.route('/highlight_message/<int:message_id>')
def highlight_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    message.highlighted = not message.highlighted  
    db.session.commit()
    flash("Message highlight status updated!", "info")
    return redirect(url_for('admin_messages'))

# Admin Dashboard Route
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session:
        flash('Please login to access the admin dashboard.', 'warning')
        return redirect(url_for('login'))

    user = user_repository.get_user_by_id(session['user_id'])
    if not user or not user.is_admin:
        if not user:
            session.pop('user_id', None)
        flash('Access denied! Admins only.', 'danger')
        return redirect(url_for('home'))

    recipes = recipe_repository.get_all_recipes()

    if request.method == 'POST':
        action = request.form.get('action')
        recipe_id = request.form.get('recipe_id')

        if action == 'delete' and recipe_id:
            recipe_repository.delete_recipe(int(recipe_id))
            flash('Recipe deleted successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        
        if action == 'edit' and recipe_id:
            return redirect(url_for('edit_recipe', recipe_id=recipe_id)) 
    return render_template('admin_dashboard.html', recipes=recipes)
'''
# Create Database and Tables
with app.app_context():
    db.create_all()
    # Check if the categories already exist; if not, insert them
    if Category.query.count() == 0: 
        category1 = Category(name="Appetizer")
        category2 = Category(name="Main Course")
        category3 = Category(name="Dessert")
        category4 = Category(name="Drinks")

        # Add categories to session
        db.session.add_all([category1, category2, category3, category4])
        db.session.commit()
        print("Categories added to the database.") '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)