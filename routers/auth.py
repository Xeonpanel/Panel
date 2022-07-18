import flask, os, hashlib

from __main__ import app, sqlquery

@app.route("/login", methods=["GET", "POST"])
def auth_login():
    if flask.request.method == "GET":
        return flask.render_template("/auth/login.html", title="Login", sqlquey=sqlquery)
    if flask.request.method == "POST":
        if flask.request.form.get("email") and flask.request.form.get("password"):
            data = sqlquery("SELECT * FROM users WHERE email = ? and password = ?", flask.request.form.get("email"), hashlib.sha256(flask.request.form.get("password").encode("utf-8")).hexdigest())
            if len(data):
                flask.session["username"] = data[0][1]
                flask.session["email"] = data[0][2]
                flask.session["id"] = data[0][0]
                flask.session["token"] = data[0][4]
                flask.session["csrf_token"] = os.urandom(250).hex()
                return flask.redirect("/dashboard")
            else:
                flask.flash("Email or password invalid", "error")
                return flask.redirect("/login")
        else:
            flask.flash("Please fill in all fields", "error")
            return flask.redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def auth_register():
    if flask.request.method == "GET":
        return flask.render_template("/auth/register.html", title="Register", sqlquey=sqlquery)
    if flask.request.method == "POST":
        if flask.request.form.get("email") and flask.request.form.get("password") and flask.request.form.get("username"):
            data = sqlquery(
                "SELECT * FROM users WHERE email = ? or name = ?",
                flask.request.form.get("email"), flask.request.form.get("username")
            )
            if len(data):
                flask.flash("User already exists", "error")
                return flask.redirect("/register")
            else:
                sqlquery(
                    "INSERT INTO users (name, email, password, token, user_type) VALUES (?, ?, ?, ?, ?)",
                    flask.request.form.get("username"),
                    flask.request.form.get("email"),
                    hashlib.sha256(
                        flask.request.form.get("password").encode("utf-8")
                    ).hexdigest(),
                    os.urandom(50).hex(),
                    "user"
                )
                flask.flash("Account created succesfully", "succes")
                return flask.redirect("/login")
        else:
            flask.flash("Please fill in all fields", "error")
            return flask.redirect("/register")