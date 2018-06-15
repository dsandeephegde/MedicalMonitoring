from app import app
from app import mysql


@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('''select * from project''')
    data = cursor.fetchall()
    if data is None:
        return "Username or Password is wrong"
    else:
        return "Database connection is working"
