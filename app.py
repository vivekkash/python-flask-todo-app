from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ge463efsqnmu'

db = SQLAlchemy(app)


class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f'{self.title} | {self.desc}'


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html", todos=Todos.query.all(), datetime=datetime)


@app.route("/add", methods=['POST'])
def addTodo():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['desc']:
            flash('Please enter both title and description', 'danger')
        else:
            todo = Todos(title=request.form['title'], desc=request.form['desc'])
            db.session.add(todo)
            db.session.commit()
            flash('New Todo records added in the list', 'success')

    return redirect(url_for("home"))


@app.route("/delete/<int:id>", methods=['GET'])
def delete(id=None):
    if id:
        Todos.query.filter_by(id=id).first()
        db.session.delete()
        db.session.commit()
        flash('Todo record deleted', 'success')

    else:
        flash('ID is empty or not found', 'danger')

    return redirect(url_for('home'))


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id=None):

        if id is None:
            flash('ID is mandatory to update record','danger')
            return redirect(url_for('home'))

        if request.method == 'POST':
            if not request.form['title'] or not request.form['desc']:
                flash('Please enter both title and description', 'danger')
                return redirect(url_for('update', id=id))

            todo = Todos.query.filter_by(id=id).first()
            if todo:
                todo.title = request.form['title']
                todo.desc = request.form['desc']
                db.session.add(todo)
                db.session.commit()
                flash('Record Updated','success')
                return redirect(url_for('home'))
            else:
                flash('No such record available to update','danger')
                return redirect(url_for('home'))
        else:
            todo = Todos.query.filter_by(id=id).first()
            if todo:
                return render_template('update.html', todo=todo)
            else:
                flash('No such record available to update','danger')
                return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True, port=8000)
