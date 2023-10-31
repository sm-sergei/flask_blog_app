from flask import Flask, render_template, flash, session, request, redirect
from flask_bootstrap import Bootstrap
import yaml, psycopg2, os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor


app = Flask(__name__)
Bootstrap(app)
CKEditor(app)

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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blogs")
    blogs = cur.fetchall()
    if blogs:
        cur.close()
        conn.close()
        return render_template('index.html', blogs=blogs)
    return render_template('index.html', blogs=None)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/blogs/<int:id>')
def blogs(id):
    """Функция возвращает кокретный блог по его id"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blogs WHERE blog_id=%s", (id,))
    blog = cur.fetchone()
    if blog:
        return render_template('blogs.html', blog=blog)
    return "<h1>Blog is not found</h1>"

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
    if request.method == "POST":
        user_details = request.form
        user_name = user_details['username']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (user_name,))
        user = cur.fetchone()
        if user:
            if check_password_hash(user[5], user_details['password']):
                session['login'] = True
                session['first_name'] = user[1]
                session['last_name'] = user[2]
                flash("Welcome, " + session['first_name'] + " " + session['last_name'] + "! You have been successfully logged in!", "success")
            else:
                cur.close()
                flash("Pssword is incorrected!", "danger")
                return render_template('login.html')
        else:
            cur.close()
            flash("User does not exist!", "danger")
            return render_template("login.html")
        cur.close()
        conn.close()
        return redirect('/')

    return render_template('login.html')

@app.route('/write-blog/', methods=['GET', 'POST'])
def write_blog():
    if request.method == "POST":
        blogpost = request.form
        title = blogpost['title']
        body = blogpost['body']
        author = session['first_name'] + " " + session['last_name']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO blogs (title, author, body) VALUES (%s, %s, %s)", (title, author, body))
        conn.commit()
        cur.close()
        conn.close()
        flash("Your blog post is successfully posted!", "success")
        return redirect('/')


    return render_template('write-blog.html')

@app.route('/my-blogs/')
def my_blogs():
    author = session['first_name'] + " " + session['last_name']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blogs WHERE author = %s", (author,))
    my_blogs = cur.fetchall()
    if my_blogs:
        return render_template('my-blogs.html', my_blogs=my_blogs)
    else:
        return render_template('my-blogs.html', my_blogs=None)


    return render_template('my-blogs.html')

@app.route('/edit-blog/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    if request.method == "POST":
        conn = get_db_connection()
        cur = conn.cursor()
        title = request.form['title']
        body = request.form['body']
        cur.execute("UPDATE blogs SET title = %s, body = %s WHERE blog_id = %s", (title, body, id))
        conn.commit()
        cur.close()
        conn.close()
        flash("Blog is updated successfully!", "success")
        return redirect("/blogs/{}".format(id))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM blogs WHERE blog_id = {}".format(id))
    blog = cur.fetchone()
    if blog:
        blog_form = {}
        blog_form['title'] = blog[1]
        blog_form['body'] = blog[3]
        return render_template('edit-blog.html', blog_form=blog_form)

@app.route('/delete-blog/<int:id>')
def delete_blog(id):
    """Функция удаляет кокретный блог по его id"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM blogs WHERE blog_id = {}".format(id))
    conn.commit()
    flash("You blog has been deleted!", "success")
    return redirect('/my-blogs')

@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logout!", "info")
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)