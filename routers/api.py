from aiohttp import payload_type
import flask, hashlib, sys, time, requests, os

from __main__ import app, sqlquery

@app.route("/api/password/<userid>/update", methods=["POST"])
def api_update_password(userid):
    if flask.session:
        if flask.request.form.get("csrf_token") == flask.session["csrf_token"]:
            data = sqlquery(
                "SELECT * FROM users WHERE password = ? and id = ?",
                hashlib.sha256(
                    flask.request.form.get("password").encode("utf-8")
                ).hexdigest(),
                userid
            )
            if len(data):
                sqlquery(
                    "UPDATE users SET password = ? WHERE password = ? and id = ?",
                    hashlib.sha256(
                        flask.request.form.get("new_password").encode("utf-8")
                    ).hexdigest(),
                    hashlib.sha256(
                        flask.request.form.get("password").encode("utf-8")
                    ).hexdigest(),
                    userid
                )
                flask.flash("Password updated succesfully", "succes")
                return flask.redirect("/dashboard/account")
            else:
                flask.flash("Password invalid", "error")
                return flask.redirect("/dashboard/account")
        else:
            flask.flash("Something went wrong", "error")
            return flask.redirect("/dashboard/account")
    else:
        flask.abort(401)

@app.route("/api/username/<userid>/update", methods=["POST"])
def api_update_username(userid):
    if flask.session:
        if flask.request.form.get("csrf_token") == flask.session["csrf_token"]:
            data = sqlquery(
                "SELECT * FROM users WHERE password = ? and id = ?",
                hashlib.sha256(
                    flask.request.form.get("password").encode("utf-8")
                ).hexdigest(),
                userid
            )
            if len(data):
                sqlquery(
                    "UPDATE users SET name = ? WHERE password = ? and id = ?",
                    flask.request.form.get("username"),
                    hashlib.sha256(
                        flask.request.form.get("password").encode("utf-8")
                    ).hexdigest(),
                    userid
                )
                flask.session["username"] = flask.request.form.get("username")
                flask.flash("Username updated succesfully", "succes")
                return flask.redirect("/dashboard/account")
            else:
                flask.flash("Password invalid", "error")
                return flask.redirect("/dashboard/account")
        else:
            flask.flash("Something went wrong", "error")
            return flask.redirect("/dashboard/account")
    else:
        flask.abort(401)

@app.route("/api/admin/settings/update", methods=["POST"])
def api_update_settings():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    sqlquery("UPDATE settings SET panel_name = ?", flask.request.form.get("panel_name"),)
                    sqlquery("UPDATE settings SET panel_logo = ?", flask.request.form["panel_logo"],)
                    flask.flash("Updated succesfully", "succes")
                    return flask.redirect("/admin")
                else:
                    flask.abort(401)
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin")
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/reboot", methods=["POST"])
def api_reboot_server():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    time.sleep(3)
                    os.execv(sys.executable, ["python"] + sys.argv)
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin")
            else:
                flask.abort(401)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/nodes/create", methods=["POST"])
def api_create_node():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    sqlquery(
                        "INSERT INTO nodes (name, memory, disk, ip, token) VALUES (?, ?, ?, ?, ?)",
                        flask.request.form.get("name"),
                        flask.request.form.get("memory"),
                        flask.request.form.get("disk"),
                        flask.request.form.get("ip"),
                        os.urandom(38).hex()
                    )
                    flask.flash("Node created succesfully", "succes")
                    return flask.redirect("/admin/nodes")
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin/nodes")
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin/nodes")
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/users/create", methods=["POST"])
def api_create_user():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    if len(sqlquery("SELECT * FROM users WHERE name = ? or email = ?", flask.request.form.get("username"), flask.request.form.get("email"))):
                        flask.flash("User already exists", "error")
                        return flask.redirect("/admin/users")
                    else:
                        sqlquery( 
                            "INSERT INTO users (name, email, password, token, user_type) VALUES (?, ?, ?, ?, ?)",
                            flask.request.form.get("username"),
                            flask.request.form.get("email"),
                            hashlib.sha256(
                                flask.request.form.get("password").encode("utf-8")
                            ).hexdigest(),
                            os.urandom(250).hex(),
                            flask.request.form.get("user_type")
                        )
                        flask.flash("User created succesfully", "succes")
                        return flask.redirect("/admin/users")
                else:
                    flask.abort(401)
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin/users")
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/users/<userid>/update", methods=["POST"])
def api_update_user(userid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form["token"])
            if len(data):
                if data[0][5] == "administrator":
                    if len(sqlquery("SELECT * FROM users WHERE id = ?", userid)):
                        if int(userid) == 1:
                            flask.flash("Cannot update master user", "error")
                            return flask.redirect("/admin/users")
                        else:
                            if flask.request.form.get("password"):
                                sqlquery(
                                    "UPDATE users SET name = ?, email = ?, password = ?, user_type = ? WHERE id = ?",
                                    flask.request.form.get("username"),
                                    flask.request.form.get("email"),
                                    flask.request.form.get("password"),
                                    flask.request.form.get("user_type"),
                                    userid
                                )
                            else:
                                sqlquery(
                                    "UPDATE users SET name = ?, email = ?, user_type = ? WHERE id = ?",
                                    flask.request.form.get("username"),
                                    flask.request.form.get("email"),
                                    flask.request.form.get("user_type"),
                                    userid
                                )
                            flask.flash("User updated succesfully", "succes")
                            return flask.redirect("/admin/users")
                    else:
                        flask.abort(404)
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin/users")
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin/users")
        else:
            flask.abort(403)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/images/create", methods=["POST"])
def api_create_image():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    sqlquery(
                        "INSERT INTO images (name, startup, image) VALUES (?, ?, ?)",
                        flask.request.form.get("image_name"),
                        flask.request.form.get("startup_command"),
                        flask.request.form.get("docker_image")
                    )
                    flask.flash("Image created succesfully", "succes")
                    return flask.redirect("/admin/images")
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin/images")
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin/images")
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/servers/create", methods=["POST"])
def api_create_server():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    if len(sqlquery("SELECT * FROM servers WHERE ip_port = ?", "{}:{}".format(sqlquery("SELECT * FROM nodes WHERE id = ?", flask.request.form.get("server_node"))[0][4], flask.request.form.get("server_port")))):
                        flask.flash("This port is already used", "error")
                        return flask.redirect("/admin/servers")
                    try:
                        server_uuid = os.urandom(13).hex()
                        payload = {
                            "system_token": sqlquery("SELECT * FROM nodes WHERE id = ?", flask.request.form.get("server_node"))[0][5],
                            "user_token": flask.request.form.get("token")
                        }
                        if requests.post("http://{}:8080/api/servers/{}/create".format(sqlquery("SELECT * FROM nodes WHERE id = ?", flask.request.form.get("server_node"))[0][4], server_uuid), data=payload).text == "server created":
                            sqlquery (
                                "INSERT INTO servers (name, memory, disk, ip_port, node_id, image_id, owner_id, suspended, uuid, image, startup) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                flask.request.form.get("server_name"),
                                flask.request.form.get("server_memory"),
                                flask.request.form.get("server_storage"),
                                "{}:{}".format(sqlquery("SELECT * FROM nodes WHERE id = ?", flask.request.form.get("server_node"))[0][4], flask.request.form.get("server_port")),
                                flask.request.form.get("server_node"),
                                flask.request.form.get("server_image"),
                                flask.request.form.get("server_owner"),
                                0,
                                server_uuid,
                                sqlquery("SELECT * FROM images WHERE id = ?", flask.request.form.get("server_image"))[0][3],
                                sqlquery("SELECT * FROM images WHERE id = ?", flask.request.form.get("server_image"))[0][2]
                            )
                            flask.flash("Server created succesfully", "succes")
                            return flask.redirect("/admin/servers")
                        else:
                            flask.flash("Something went wrong", "error")
                            return flask.redirect("/admin/servers")
                    except:
                        flask.flash("The node is currently offline", "error")
                        return flask.redirect("/admin/servers")
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin/servers")
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin/servers")
        else:
            flask.abort(403)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/images/<imageid>/update", methods=["POST"])
def api_update_image(imageid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    sqlquery(
                        "UPDATE images SET name = ?, startup = ?, image = ? WHERE id = ?",
                        flask.request.form.get("image_name"),
                        flask.request.form.get("startup_command"),
                        flask.request.form.get("docker_image"),
                        imageid
                    )
                    flask.flash("Image updated succesfully", "succes")
                    return flask.redirect("/admin/images/{}/view".format(imageid))
                else:
                    flask.abort(401)
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin/images/{}/view".format(imageid))
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/images/<imageid>/variables/create", methods=["POST"])
def api_create_variable(imageid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    sqlquery(
                        "INSERT INTO image_variables (name, variable, data, image_id) VALUES (?, ?, ?, ?)",
                        flask.request.form.get("variable_name"),
                        flask.request.form.get("variable"),
                        flask.request.form.get("variable_data"),
                        imageid
                    )
                    flask.flash("Variable created succesfully", "succes")
                    return flask.redirect("/admin/images/{}/view".format(imageid))
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin/images/{}/view".format(imageid))
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin/images/{}/view".format(imageid))
        else:
            flask.abort(403)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/images/<imageid>/variables/<variableid>/update", methods=["POST"])
def api_update_variable(imageid, variableid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    sqlquery(
                        "UPDATE image_variables SET name = ?, variable = ?, data = ? WHERE id = ?",
                        flask.request.form.get("variable_name"),
                        flask.request.form.get("variable"),
                        flask.request.form.get("variable_data"),
                        variableid
                    )
                    flask.flash("Variable updated succesfully", "succes")
                    return flask.redirect("/admin/images/{}/view".format(imageid))
                else:
                    flask.abort(401)
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin/images/{}/view".format(imageid))
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/images/<imageid>/variables/<variableid>/delete", methods=["POST"])
def api_delete_variable(imageid, variableid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = sqlquery("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    sqlquery("DELETE FROM image_variables WHERE id = ? and image_id = ?", variableid, imageid)
                    flask.flash("Variable deleted succesfully", "succes")
                    return flask.redirect("/admin/images/{}/view".format(imageid))
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin/images/{}/view".format(imageid))
            else:
                flask.abort(401)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")