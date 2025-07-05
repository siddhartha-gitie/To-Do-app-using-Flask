from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

todos = []
next_id = 1

TEMPLATE = """
<!doctype html>
<html>
  <head>
    <title>To-Do List</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background: #f4f4f4;
        padding: 20px;
        max-width: 600px;
        margin: auto;
      }
      h1 {
        text-align: center;
        color: #333;
      }
      form {
        display: flex;
        margin-bottom: 20px;
      }
      input[type="text"] {
        flex: 1;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 4px 0 0 4px;
      }
      button {
        padding: 10px 20px;
        border: none;
        background: #28a745;
        color: white;
        border-radius: 0 4px 4px 0;
        cursor: pointer;
      }
      button:hover {
        background: #218838;
      }
      ul {
        list-style: none;
        padding: 0;
      }
      li {
        background: white;
        padding: 10px;
        margin-bottom: 8px;
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .links a {
        text-decoration: none;
        color: #007bff;
        margin-left: 10px;
      }
      .links a:hover {
        text-decoration: underline;
      }
    </style>
  </head>
  <body>
    <h1>To-Do List</h1>
    <form method="post" action="/add">
      <input type="text" name="task" autocomplete="off" placeholder="Enter a new task" required>
      <button type="submit">Add</button>
    </form>
    <ul>
      {% for todo in todos %}
        <li>
          <span>
            {{ todo['task'] }} - {% if todo['done'] %}<strong>Done</strong>{% else %}Not Done{% endif %}
          </span>
          <span class="links">
            {% if not todo['done'] %}
              <a href="{{ url_for('mark_done', todo_id=todo['id']) }}">Mark Done</a>
            {% endif %}
            <a href="{{ url_for('delete_todo', todo_id=todo['id']) }}">Delete</a>
          </span>
        </li>
      {% endfor %}
    </ul>
  </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(TEMPLATE, todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    global next_id
    task = request.form['task']
    todos.append({'id': next_id, 'task': task, 'done': False})
    next_id += 1
    return redirect(url_for('index'))

@app.route('/done/<int:todo_id>')
def mark_done(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['done'] = True
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
