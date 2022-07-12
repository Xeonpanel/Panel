import flask, os

from __main__ import app, sqlquery

@app.route("/login", methods=["GET", "POST"])
def login():
    if os.path.isfile("database.db"):
        if flask.request.method == "GET":
            return flask.render_template(
                "themes/{}/auth/login.html".format(app.config["THEME"]),
                title="Login"
            )
        elif flask.request.method == "POST":
            try:
                if flask.request.form["email"] and flask.request.form["password"]:
                    data = sqlquery("SELECT * FROM users WHERE email = ? and password = ?", flask.request.form["email"], flask.request.form["password"]).fetchall()
                    if len(data):
                        flask.session["username"] = data[0][1]
                        flask.session["email"] = data[0][2]
                        flask.session["id"] = data[0][0]
                        flask.session["api_key"] = data[0][5]
                        flask.session["user_type"] = data[0][4]
                        flask.session["csrf_token"] = os.urandom(250).hex()
                        return flask.redirect("/dashboard")
                    else:
                        flask.flash("Email or password invalid", "error")
                        return flask.redirect("/login")
            except:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/login")
    else:
        return flask.redirect("/setup/getting-started")