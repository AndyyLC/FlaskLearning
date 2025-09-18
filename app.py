#Imports

from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DatabaseAlchemy.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<Task {self.id}>"
        
@app.route('/',methods=["POST","GET"])
def index():
    if request.method == "POST":
        current_task = request.form['content']
        new_task = Task(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"An error occurred while adding the task: {e}")
            return f"An error occurred while adding the task: {e}"
    else:
        tasks = Task.query.order_by(Task.createdAt).all()
        return render_template('index.html', tasks = tasks)
    
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = Task.query.get_or_404(id)
    try: 
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"An error occurred while deleting the task: {e}")
        return f"An error occurred while deleting the task: {e}"

@app.route('/update/<int:id>', methods=["POST","GET"])
def edit(id:int):
    task=Task.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content'] # changes current task content to new content that is in the form

        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"An error occurred while updating the task: {e}")
            return f"An error occurred while updating the task: {e}"
        
    else:
        return render_template('edit.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

app.run(debug=True)