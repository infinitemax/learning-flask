import sys
from werkzeug.utils import redirect
from application import app
from flask import render_template, request, flash, url_for
from .forms import TodoForm
from application import db
from datetime import datetime
from bson import ObjectId

# rendering an html file from the templates folder
@app.route("/")
def get_todos():
    todos = []
    for todo in db.todo_flask.find().sort({"date_created": -1}):
        todo["_id"] = str(todo["_id"])
        todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M%S")
        todos.append(todo)

    return render_template("view_todos.html", title = "layout page", todos = todos)

@app.route("/add_todo", methods=["POST", "GET"])
def add_todo():
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todo_flask.insert_one({
            "name" : todo_name,
            "description" : todo_description,
            "completed" : completed,
            "date_created" : datetime.utcnow()
        })

        flash("Added successully!", "success")
        
        return redirect("/")
    
    else: 
        form = TodoForm()
    return render_template("add_todo.html", form = form)

# update the item
@app.route("/update_todo/<id>", methods = ["POST", "GET"])
def update_todo(id):
    if request.method == "POST":
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        completed = form.completed.data

        db.todo_flask.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name" : todo_name,
            "description" : todo_description,
            "completed" : completed,
            "date_created" : datetime.utcnow()
        }})

        flash("todo updated", "success")
        return redirect("/")

    # this bit renders the prefilled form
    else:
        form = TodoForm()

        todo = db.todo_flask.find_one_or_404({"_id" : ObjectId(id)})
        form.name.data = todo.get("name", None)
        form.description.data = todo.get("description", None)
        form.completed.data = todo.get("completed", None)
    
    return render_template("add_todo.html", form = form)

@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todo_flask.find_one_and_delete({"_id": ObjectId(id)})
    flash("item deleted")
    return redirect("/")