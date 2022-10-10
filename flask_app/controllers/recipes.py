from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import recipe , user


@app.route("/recipes/new")
def create_recipe_link():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("new_recipe.html" , this_user = user.User.get_user_by_id(data))

@app.route("/recipes/add_to_db" , methods=["POST"])
def add_recipe_to_db():
    if not recipe.Recipe.validate_form(request.form):
        return redirect("/recipes/new")
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_created": request.form["date_created"],
        "under_hour": request.form["under_hour"],
        "user_id": session["user_id"]
    }
    recipe.Recipe.create_recipe(data)
    return redirect("/recipes")


@app.route("/recipes/<int:id>")
def view_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    return render_template("show_recipe.html", this_recipe = recipe.Recipe.get_a_recipe(data), this_user = user.User.get_user_by_id(data))

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    return render_template("edit_recipe.html", this_recipe = recipe.Recipe.get_a_recipe(data), this_user = user.User.get_user_by_id(data))


@app.route("/recipes/edit_in_db/<int:id>" , methods=["POST"])
def edit_recipe_in_db(id):
    if not recipe.Recipe.validate_form(request.form):
        return redirect(f"/recipes/edit/{id}")
    if "user_id" not in session:
        return redirect("/")
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_created": request.form["date_created"],
        "under_hour": request.form["under_hour"],
        "id": id,
    }
    recipe.Recipe.edit_recipe(data)
    return redirect("/recipes")

@app.route("/recipes/delete_in_db/<int:id>")
def delete_recipe_in_db(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id":id
    }
    recipe.Recipe.delete_recipe(data)
    return redirect("/recipes")