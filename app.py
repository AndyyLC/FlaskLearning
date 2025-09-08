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
        
@app.route('/',methods=['POST,GET'])
def index():
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = Task(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"An error occurred while adding the task: {e}")
            return f"An error occurred while adding the task: {e}"
        


    return render_template('index.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)