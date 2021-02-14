from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#tells our app where our database is located
#3 forward slashes is relative path and 4 is abosoute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#initialize database with settings from our app
db = SQLAlchemy(app)

#make model
class Todo(db.Model):
  #make our columns:
  #id for each entry
  id = db.Column(db.Integer, primary_key=True)
  #content column, type String, max length 200, and can't be null
  content = db.Column(db.String(200), nullable=False)
  #add created date automatically
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  #func that will return a string whenever we create a new element
  def __repr__(self):
    #returns the Task and the id of that task
    return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET']) #this route can now accept 2 methods instead of just GET
def index():
  #if the request that is sent to this route is a POST
  if request.method == 'POST':
    #gets the content from the submitted form
    task_content = request.form['content']
    #create new Todo instance using the submitted content
    new_task = Todo(content=task_content)
   
    try:
      #adds task to db
      db.session.add(new_task)
      #commits the add
      db.session.commit()
      #redirects to index page
      return redirect('/')
    except:
      #returns string in case of failure
      return 'There was an issue adding your task'
  else:
    #if it's not a POST request then we just want to show a list of tasks
    #query the DB for all the task and sort by date created
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks) #passes all the tasks to the template


  return render_template('index.html')


@app.route('/delete/<int:id>')
def delete(id):
  #query the db to find the task that we want to delete
  #if it's not found, then return 404 error
  task_to_delete = Todo.query.get_or_404(id)

  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  #query db for task that matches the id
  task = Todo.query.get_or_404(id)

  #if we are updating with a POST
  if request.method == 'POST':
    #change the content of the task to the content inputted into request form
    task.content = request.form['content']

    try:
      #if we successfully commit changes then we redirect to the home page
      db.session.commit()
      return redirect('/')
    except:
      return 'There an issue updating your task'
  else:
    #else just return the current task content
    return render_template('update.html', task=task)

if __name__ == "__main__":
  app.run(debug=True)