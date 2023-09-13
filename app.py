from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy()

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
db.init_app(app)
app.app_context().push()
db.create_all()

@app.route("/", methods = ['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        title = (request.form['title'])
        desc = (request.form['desc'])
        try:
            completed = bool(request.form['completed'])
        except:
            completed = False #if an error occurs, it means no input is received which means checbox was not checked
        todo = ToDo(title=title, desc=desc, completed=completed)
        db.session.add(todo)
        db.session.commit()
    allToDo = ToDo.query.all()
    return render_template('index.html', allToDo=allToDo)

@app.route("/tasks")
def products():
    allToDo = ToDo.query.all()
    print(allToDo)
    return 'This is the products page'

@app.route("/update/<int:sno>", methods = ['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = (request.form['title'])
        desc = (request.form['desc'])
        try:
            completed = bool(request.form['completed'])
        except:
            completed = False #if an error occurs, it means no input is received which means checbox was not checked
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        todo.completed=completed
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = ToDo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8000)
