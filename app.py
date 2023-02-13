from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # Defines a relative path for the database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Variable to store the database

# Specifies a model for a Todo entry into the database
# Defines an integer column for the id, a string column for the title, and a boolean column for complete
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Home route displays the base template and populates it with all the todos from the database
@app.route('/')
def home():
    todo_list = Todo.query.all() # List of all the items in the database
    return render_template('base.html', todo_list=todo_list) # Renders the html based on the template and passes the todo_list variable to it

# Is called by the add form
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title") # Fetches the title from the user input
    new_todo = Todo(title=title, complete=False) # Creates a new todo from the model
    db.session.add(new_todo) # Adds the new todo to the database
    db.session.commit() # Commits it to the session
    return redirect(url_for("home")) # Redirects back home

# Update route toggles the todo items complete state
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() # Finds the todo item being updated
    todo.complete = not todo.complete # Toggles the complete boolean
    db.session.commit() # Commits it to the session
    return redirect(url_for("home")) # Redirects back home

# Delete route removes the item from the database
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() # Finds the todo item being deleted
    db.session.delete(todo) # Deletes the todo item from the database
    db.session.commit() # Commits it to the session
    return redirect(url_for("home")) # Redirects back home

if __name__ == "__main__":
    # Creates the database
    with app.app_context():
        db.create_all()
    # Runs the app in debug mode
    app.run(debug=True)