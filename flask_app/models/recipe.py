from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user 

class Recipe:
    def __init__(self,db_data):
        self.id = db_data["id"]
        self.name = db_data["name"]
        self.description = db_data["description"]
        self.instructions = db_data["instructions"]
        self.date_created = db_data["date_created"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]
        self.under_hour = db_data["under_hour"]
        self.user = None

    @classmethod
    def create_recipe(cls, data):
        query = """
            INSERT INTO recipes
            (name, description, instructions, date_created, user_id, under_hour)
            VALUES
            (%(name)s, %(description)s, %(instructions)s, %(date_created)s, %(user_id)s, %(under_hour)s);
            """
        return connectToMySQL("recipes_schema").query_db(query, data)

    @classmethod
    def get_all_recipes(cls):
        query = """
            SELECT * FROM recipes 
            JOIN users 
            ON recipes.user_id = users.id;
            """
        results = connectToMySQL("recipes_schema").query_db(query)
        print(results)
        if len(results) == 0:
            return []
        else:
            all_recipes_objects = []
            for recipe_dictionary in results:
                recipe_obj = Recipe(recipe_dictionary)
                user_dictionary = {
                    "id": recipe_dictionary["users.id"],
                    "first_name": recipe_dictionary["first_name"],
                    "last_name": recipe_dictionary["last_name"],
                    "email": recipe_dictionary["email"],
                    "password": recipe_dictionary["password"],
                    "created_at": recipe_dictionary["users.created_at"],
                    "updated_at": recipe_dictionary["users.updated_at"],
                }
                user_obj = user.User(user_dictionary)
                recipe_obj.user = user_obj
                all_recipes_objects.append(recipe_obj)
            return all_recipes_objects


    @classmethod
    def get_a_recipe(cls , data):
        query = """
            SELECT * FROM recipes 
            JOIN users 
            ON recipes.user_id = users.id
            WHERE recipes.id = %(id)s;
            """
        results = connectToMySQL("recipes_schema").query_db(query, data)
        print(results)
        if len(results) == 0:
            return None
        else:
            recipe_obj = Recipe(results[0])
            user_dictionary = {
                "id": results[0]["users.id"],
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "email": results[0]["email"],
                "password": results[0]["password"],
                "created_at": results[0]["users.created_at"],
                "updated_at": results[0]["users.updated_at"],
            }
            user_obj = user.User(user_dictionary)
            recipe_obj.user = user_obj
        return recipe_obj

    @classmethod
    def edit_recipe(cls, data):
        query = """
        UPDATE recipes SET
        name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s,
        date_created = %(date_created)s,
        under_hour = %(under_hour)s
        WHERE 
        id = %(id)s;
        """
        return connectToMySQL("recipes_schema").query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = """
        DELETE FROM recipes
        WHERE 
        id = %(id)s
        """
        return connectToMySQL("recipes_schema").query_db(query, data)


    @staticmethod
    def validate_form(form_data):
        is_valid = True
        if len(form_data["name"]) < 3:
            flash("Name must be at least 3 characters" , "form")
            is_valid = False
        if len(form_data["description"]) < 3:
            flash("Description must be at least 3 characters" , "form")
            is_valid = False
        if len(form_data["instructions"]) < 3:
            flash("Instructions must be at least 3 characters" , "form")
            is_valid = False
        if "under_hour" not in form_data:
            flash("When did you cook it?" , "form")
            is_valid = False
        if "under_hour" not in form_data:
            flash("Did it take 30 minutes to cook?" , "form")
            is_valid = False
        return is_valid

