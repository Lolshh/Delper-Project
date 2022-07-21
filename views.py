from flask import Blueprint, render_template, request, redirect
import sqlite3

views = Blueprint(__name__, "views")
active_session = False
active_id = -1


@views.route("/")
def home():
    if active_session:
        with sqlite3.connect("delper.db") as con:
            curr = con.cursor()
            curr_id = curr.execute('SELECT * FROM users WHERE (ID=?)', (active_id,))
            return render_template("index.html", data=str(curr_id.fetchone()[0]))
    return render_template("index.html", data="UNDEFINED")


@views.route("/register", methods=["GET", "POST"])
def register():
    with sqlite3.connect("delper.db") as con:
        if request.method == "POST":
            curr = con.cursor()
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            passwordcheck = request.form.get('passwordCheck')
            newsletter = request.form.get('newsletter')

            # Check when enter is pressed why creating

            if password != passwordcheck:
                return render_template("register.html", message="Passwords do not match.")
            UsernameCheck = curr.execute('SELECT * FROM users WHERE (USERNAME=?)', (username,))
            EmailCheck = curr.execute('SELECT * FROM users WHERE (Email=?)', (email,))
            UsernameCheckExists = UsernameCheck.arraysize > 0 and UsernameCheck.fetchone() is not None
            EmailCheckExists = EmailCheck.arraysize > 0 and EmailCheck.fetchone() is not None
            if UsernameCheckExists and EmailCheckExists:
                return render_template('register.html', message="It seems that you do not have an account yet... Let's "
                                                                "create one !")
            elif UsernameCheckExists:
                return render_template('register.html', message="Please choose another username.")
            elif EmailCheckExists:
                return render_template('register.html', message="This email address is already linked with an account.")
            else:
                user_id = curr.execute("SELECT COUNT(*) FROM users")
                curr.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?)',
                             (username, email, password, newsletter, user_id.fetchone()[0]))
                return redirect("/")
    return render_template("register.html")


@views.route("/login", methods=["GET", "POST"])
def login():
    with sqlite3.connect("delper.db") as con:
        if request.method == "POST":
            curr = con.cursor()
            username = request.form.get('username')
            password = request.form.get('password')

            accountExists = curr.execute("SELECT * FROM users WHERE (USERNAME = ? and PASSWORD = ?)",
                                         (username, password))
            size = accountExists.arraysize
            specificAccount = accountExists.fetchone()

            if size == 1 and specificAccount is not None:
                global active_id
                global active_session
                active_id = specificAccount[-1]
                active_session = True
                return redirect("/")
            else:
                return render_template("login.html", message="Wrong username or password. Please try again.")
    return render_template("login.html")


@views.route("/logout")
def logout():
    global active_id
    global active_session
    active_id = -1
    active_session = False
    return render_template("index.html", data="UNDEFINED")


@views.route("/account")
def account():
    return render_template("account.html", message =" ")
    with sqlite3.connect("delper.db") as con:
        curr = con.cursor()
        curr_id = curr.execute('SELECT * FROM users WHERE (ID=?)', (active_id,))
    return render_template("account.html", message=str(curr_id.fetchone()[0])) if active_session else render_template("noaccount.html")


@views.route("/services")
def services():
    if active_session:
        return render_template("services.html", data=active_id)
    return render_template("services.html", data="UNDEFINED")


@views.route("/contact")
def contact():
    if active_session:
        return render_template("contact.html", data=active_id)
    return render_template("contact.html", data="UNDEFINED")


@views.route("/services/pythonShowRoom")
def pythonshowroom():
    return render_template("ShowRoom/pythonShowRoom.html")


@views.route("/services/solidityShowRoom")
def solidityshowroom():
    return render_template("ShowRoom/solidityShowRoom.html")


@views.route("/services/javaShowRoom")
def javashowroom():
    return render_template("ShowRoom/javaShowRoom.html")


@views.route("/services/javascriptShowRoom")
def javascriptshowroom():
    return render_template("ShowRoom/javascriptShowRoom.html")


@views.route("/services/htmlShowRoom")
def htmlshowroom():
    return render_template("ShowRoom/htmlShowRoom.html")


@views.route("/services/cssShowRoom")
def cssshowroom():
    return render_template("ShowRoom/cssShowRoom.html")


