from datetime import date
import sqlite3
from flask import Blueprint, render_template, request, redirect

views = Blueprint(__name__, "views")
active_session = False
godmode = False
active_id = -1


@views.route("/")
def home():
    if active_session:
        return render_template("index.html", data="DEFINED")
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
            today = date.today()

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
                user_id = curr.execute("SELECT COUNT(*) FROM users").fetchone()[0]
                curr.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)',
                             (username, email, password, newsletter, today, False, user_id))
                global active_id
                global active_session
                active_session = True
                active_id = user_id
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
                global godmode
                active_id = specificAccount[-1]
                active_session = True
                if list(specificAccount)[-2]:
                    godmode = True
                    active_id = 0
                return redirect("/")
            else:
                return render_template("login.html", message="Wrong username or password. Please try again.")
    return render_template("login.html")


@views.route("/logout")
def logout():
    global active_id
    global active_session
    global godmode
    active_id = -1
    active_session = False
    godmode = False
    return render_template("index.html", data="UNDEFINED")


@views.route("/account", methods=["GET", "POST"])
def account():
    global godmode
    global active_id
    if active_session:
        with sqlite3.connect("delper.db") as con:
            curr = con.cursor()
            user_info = list(curr.execute('SELECT * FROM users WHERE ID = ?', (active_id,)).fetchone())
            if not (godmode and active_id == 0):
                proj = list(curr.execute('SELECT * FROM projects WHERE USER_ID = ? ORDER BY PROJECT_ID', (active_id,)))
                return render_template("account.html", message=" ", data=proj, date=user_info[-3],
                                       username=user_info[0])
            else:
                return redirect("/godmode")
    else:
        return render_template("noaccount.html")


@views.route("/createProject", methods=["GET", "POST"])
def create_project():
    with sqlite3.connect("delper.db") as con:
        if request.method == "POST":
            curr = con.cursor()
            project_id = curr.execute("SELECT COUNT(*) FROM projects WHERE USER_ID = ?", (active_id,))
            title = request.form.get('projectTitle')
            description = request.form.get('projectDescription')
            languages = request.form.getlist('languagePicker')
            languages = ', '.join(languages)
            curr.execute('INSERT INTO projects VALUES(?, ?, ?, ?, ?)',
                         (active_id, project_id.fetchone()[0], title, description, languages))
    return redirect('/account')


@views.route("/godmode", methods=["GET", "POST"])
def godmode():
    global godmode
    global active_id
    if not godmode:
        return redirect("/")
    with sqlite3.connect("delper.db") as con:
        if request.method == "POST":
            active_id = int(request.form.get("userID"))
            return redirect("/account")
    return render_template("godmodeView.html")


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
