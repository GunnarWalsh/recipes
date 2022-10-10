from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.models import recipe


class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = []
        

    @staticmethod
    def validate_reg(form_data):
        is_valid = True
        if len(form_data["first_name"]) < 2:
            flash("First name must be 2 or more characters" , "register")
            is_valid = False
        if len(form_data["last_name"]) < 2:
            flash("Last name must be 2 or more characters" , "register")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(form_data["password"]) < 8:
            flash("Password must be 8 or more characters" , "register")
            is_valid = False
        if form_data["password"] != form_data["confirm_password"]:
            flash("Passwords did not match!")
        return is_valid

    @classmethod
    def register_user(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL("recipes_schema").query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL("recipes_schema").query_db(query, data)
        if len(results) == 0:
            return None
        else: 
            return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL("recipes_schema").query_db(query, data)
        if len(results) == 0:
            return None
        else: 
            return cls(results[0])


    @classmethod 
    def get_user_recipes(cls, data):
        query = """
        SELECT * FROM users 
        LEFT JOIN recipes 
        ON recipes.user_id = users.id 
        WHERE id = %(id)s;
        """
        results = connectToMySQL("recipes_schema").query_db(query, data)
        if len(results) == 0:
            return None
        else: 
            this_user_object = cls(results[0])
            for this_recipe in results:
                this_recipe_dictionary = {
                    "id": this_recipe["recipes.id"],
                    "name": this_recipe["name"],
                    "description": this_recipe["description"],
                    "instructions": this_recipe["instructions"],
                    "date_created": this_recipe["date_created"],
                    "created_at": this_recipe["recipes.created_at"],
                    "updated_at": this_recipe["recipes.updated_at"],
                    "under_hour": this_recipe["under_hour"],
                }
                this_recipe_obj = recipe.Recipe(this_recipe_dictionary)
                this_user_object.recipes.append(this_recipe_obj)
            return this_user_object

    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Something is off! Try again!" , "login")
            return False
        data = {
            "email": form_data["email"]
        }    
        got_user = User.get_user_by_email(data)
        if got_user == None:
            flash("Something is off! Try again!", "login")
            return False
        if not bcrypt.check_password_hash(got_user.password, form_data["password"]):
            flash("Something is off! Try again!", "login")
            return False 
        return got_user

