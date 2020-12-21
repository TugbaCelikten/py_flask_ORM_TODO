from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# --------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Python_Calisma/ToDoApp_ORM_Sqlite3/todo.db'
db = SQLAlchemy(app)

# --------------------


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

# --------------------


@app.route("/")
def index():
    todos = ToDo.query.all()
    return render_template("index.html", todos=todos)

# --------------------


@app.route("/complete/<string:id>")
def completeToDo(id):
    todo = ToDo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()

    return redirect(url_for("index"))

# --------------------


@app.route("/delete/<string:id>")
def deleteToDo(id):
    todo = ToDo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

# --------------------


@app.route("/add", methods=["POST"])
def addToDo():
    title = request.form.get("title")
    newToDo = ToDo(title=title, complete=False)
    db.session.add(newToDo)
    db.session.commit()

    return redirect(url_for("index"))

# --------------------


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
