import flask, os
from __main__ import app, db, bcrypt
from models import Users

@app.get("/login")
def getlogin():
    return flask.render_template("/auth/login.html", title="Login", page="auth.login")

@app.get("/register")
def getregister():
    return flask.render_template("/auth/register.html", title="Register", page="auth.register")

@app.post("/login")
def postlogin():
    username = flask.request.json.get("username")
    password = flask.request.json.get("password")
    if username and password:
        user = Users.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            flask.session["user_id"] = user.id
            flask.session["admin"] = user.admin
            flask.session["csrf_token"] = os.urandom(50).hex()
            return flask.redirect("/dashboard")
        else:
            return flask.jsonify({"status": "error", "message": "Invalid username or password"})

@app.post("/register")
def postregister():
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    email = flask.request.form.get("email")
    if username and password and email:
        if Users.query.filter_by(username=username).first():
            return flask.jsonify({"status": "error", "message": "Username already exists"})
        elif Users.query.filter_by(email=email).first():
            return flask.jsonify({"status": "error", "message": "Email already exists"})
        else:
            user = Users(username=username, password=bcrypt.generate_password_hash(password), email=email, admin=False, created_at=flask.datetime.datetime.now(), updated_at=flask.datetime.datetime.now())
            db.session.add(user)
            db.session.commit()
            return flask.jsonify({"status": "success", "message": "Account created"})
    else:
        return flask.jsonify({"status": "error", "message": "Please fill in all fields"})
