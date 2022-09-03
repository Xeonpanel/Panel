import flask, os, hashlib

from __main__ import app, query

@app.get("/login")
def getlogin():
    return flask.render_template("/auth/login.html", title="Login")

@app.get("/register")
def getregister():
    return flask.render_template("/auth/register.html", title="Register")

@app.post("/login")
def postlogin():
    if flask.request.form.get("email") and flask.request.form.get("password"):
        data = query("SELECT * FROM users WHERE email = ? and password = ?", flask.request.form.get("email"), hashlib.sha256(flask.request.form.get("password").encode("utf-8")).hexdigest())
        if len(data):
            flask.session["username"] = data[0][1]
            flask.session["email"] = data[0][2]
            flask.session["id"] = data[0][0]
            flask.session["token"] = data[0][4]
            flask.session["csrf_token"] = os.urandom(250).hex()
            return flask.jsonify({"status": "succes"})
        else:
            return flask.jsonify({"status": "error", "message": "Email or password invalid"})
    else:
        return flask.jsonify({"status": "error", "message": "Please fill in all fields"})

# @app.route("/register", methods=["GET", "POST"])
# def auth_register():
#     if flask.request.method == "GET":
#         return flask.render_template("/auth/register.html", title="Register", sqlquey=query)
#     if flask.request.method == "POST":
#         if flask.request.form.get("email") and flask.request.form.get("password") and flask.request.form.get("username"):
#             data = query(
#                 "SELECT * FROM users WHERE email = ? or name = ?",
#                 flask.request.form.get("email"), flask.request.form.get("username")
#             )
#             if len(data):
#                 return flask.jsonify({"status": "error", "message": "Username or email already exists"})
#             else:
#                 query(
#                     "INSERT INTO users (name, email, password, token, user_type) VALUES (?, ?, ?, ?, ?)",
#                     flask.request.form.get("username"),
#                     flask.request.form.get("email"),
#                     hashlib.sha256(
#                         flask.request.form.get("password").encode("utf-8")
#                     ).hexdigest(),
#                     os.urandom(50).hex(),
#                     "user"
#                 )
#                 return flask.jsonify({"status": "succes"})
#         else:
#             return flask.jsonify({"status": "error", "message": "Please fill in all fields"})