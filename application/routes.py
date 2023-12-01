from flask.templating import render_template_string
from werkzeug.datastructures import RequestCacheControl
from werkzeug.utils import redirect
from application import app
from flask import render_template, request, flash
from .forms import TodoForm
from application import db
from datetime import datetime

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