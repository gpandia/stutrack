from flask import Flask, request, render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    doer=db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.ID

@app.route('/',methods=['POST','GET'])
def index():
    if request.method =='POST':
        task_content=request.form['book']  
        task_doer=request.form['chapter']

        new_task=Todo(content=task_content,doer=task_doer)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "❌ There was an issue adding your task."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return '❌ There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['book']
        task.doer = request.form['chapter']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return '❌ There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


@app.route('/deleteall/all')
def deleteall():
    try:
        db.session.query(Todo).delete()
        db.session.commit()
        return redirect('/')
    except:
        return '❌ There was a problem deleting.'


if __name__=="__main__":
    app.run(debug=True)
