from flask import Flask, render_template, flash, session, request, redirect
from flask_bootstrap import Bootstrap
import yaml, psycopg2, os
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = os.urandom(24)

#DB Configuration
db = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)

def get_db_connection():
    conn = psycopg2.connect(host=db['pg_host'],
                            database=db['pg_db'],
                            user=db['pg_user'],
                            password=db['pg_password'])
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/blogs/<int:id>')
def blogs(id):
    """Функция возвращает кокретный блог по его id"""
    return render_template('blogs.html', blog_id=id)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user_details = request.form
        if user_details['password'] != user_details['ConfirmPassword']:
            flash("Passwords do not match! Try it again!", "danger")
            return render_template('register.html')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users(first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s)",
                    (user_details['firstname'],
                    user_details['lastname'],
                    user_details['username'],
                    user_details['email'],
                    generate_password_hash(user_details['password'])))
        conn.commit()
        cur.close()
        flash("Registratiomn successfull! Please login", "success")
        return  redirect('/login/')
    return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/write-blog/', methods=['GET', 'POST'])
def write_blog():
    return render_template('write-blog.html')

@app.route('/my-blogs/')
def my_blogs():
    return render_template('my-blogs.html')

@app.route('/edit-blog/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    return render_template('edit-blog.html', blog_id=id)

@app.route('/delete-blog/<int:id>', methods=['POST'])
def delete_blog(id):
    """Функция удаляет кокретный блог по его id"""
    return 'Successfully deleted!'

@app.route('/logout/')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)