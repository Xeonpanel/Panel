import flask, requests, os, sys, time

from __main__ import app, sqlquery

@app.route("/api/admin/settings", methods=["POST"])
def api_settings():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form["csrf_token"]:
            data = sqlquery("SELECT * FROM users WHERE api_key = ?", flask.request.form["api_key"]).fetchall()
            if len(data):
                if data[0][4] == "administrator":
                    sqlquery("UPDATE settings SET panel_name = ?", flask.request.form["panel_name"],)
                    flask.flash("Panel name updated succesfully", "succes")
                    return flask.redirect("/admin")
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin")
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin")
        else:
            flask.abort(403)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/reboot", methods=["POST"])
def api_reboot():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form["csrf_token"]:
            data = sqlquery("SELECT * FROM users WHERE api_key = ?", flask.request.form["api_key"]).fetchall()
            if len(data):
                if data[0][4] == "administrator":
                    time.sleep(3)
                    os.execv(sys.executable, ["python"] + sys.argv)
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin")
            else:
                flask.flash("Something went wrong", "error")
                return flask.redirect("/admin")
        else:
            flask.abort(403)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/nodes/create", methods=["POST"])
def api_createnode():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form["csrf_token"]:
            data = sqlquery("SELECT * FROM users WHERE api_key = ?", flask.request.form["api_key"]).fetchall()
            if len(data):
                if data[0][4] == "administrator":
                    sqlquery(
                        "INSERT INTO nodes (name, ip, memory, disk, node_api) VALUES (?, ?, ?, ?, ?)",
                        flask.request.form["node_name"],
                        flask.request.form["ip_address"],
                        flask.request.form["node_memory"],
                        flask.request.form["node_storage"],
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
            flask.abort(403)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/users/create", methods=["POST"])
def api_createuser():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form["csrf_token"]:
            data = sqlquery("SELECT * FROM users WHERE api_key = ?", flask.request.form["api_key"]).fetchall()
            if len(data):
                if data[0][4] == "administrator":
                    sqlquery( 
                        "INSERT INTO users (username, email, password, user_type, api_key) VALUES (?, ?, ?, ?, ?)",
                        flask.request.form["username"],
                        flask.request.form["email"],
                        flask.request.form["password"],
                        flask.request.form["user_type"],
                        os.urandom(250).hex()
                    )
                    flask.flash("User created succesfully", "succes")
                    return flask.redirect("/admin/users")
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

@app.route("/api/admin/users/<userid>/update", methods=["POST"])
def api_updateuser(userid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form["csrf_token"]:
            data = sqlquery("SELECT * FROM users WHERE api_key = ? and id = ?", flask.request.form["api_key"], int(userid)).fetchall()
            if len(data):
                if data[0][4] == "administrator":
                    if flask.request.form["password"]:
                        sqlquery(
                            "UPDATE users SET username = ?, email = ?, password = ?, user_type = ? WHERE id = ?",
                            flask.request.form["username"],
                            flask.request.form["email"],
                            flask.request.form["password"],
                            flask.request.form["user_type"],
                            int(userid)
                        )
                    else:
                        sqlquery(
                            "UPDATE users SET username = ?, email = ?, user_type = ? WHERE id = ?",
                            flask.request.form["username"],
                            flask.request.form["email"],
                            flask.request.form["user_type"],
                            int(userid)
                        )
                    flask.flash("User updated succesfully", "succes")
                    return flask.redirect("/admin/users")
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
def api_createimage():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form["csrf_token"]:
            data = sqlquery("SELECT * FROM users WHERE api_key = ?", flask.request.form["api_key"]).fetchall()
            if len(data):
                if data[0][4] == "administrator":
                    sqlquery(
                        "INSERT INTO images (name, startup_command, docker_image) VALUES (?, ?, ?)",
                        flask.request.form["image_name"],
                        flask.request.form["startup_command"],
                        flask.request.form["docker_image"]
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
            flask.abort(403)
    else:
        return flask.redirect("/login")

@app.route("/api/admin/servers/create", methods=["POST"])
def api_createserver():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form["csrf_token"]:
            data = sqlquery("SELECT * FROM users WHERE api_key = ?", flask.request.form["api_key"]).fetchall()
            if len(data):
                if data[0][4] == "administrator":
                    owner_email = sqlquery("SELECT * FROM users WHERE id = ?", flask.request.form["server_owner"]).fetchall()[0][2]
                    owner_api = sqlquery("SELECT * FROM users WHERE id = ?", flask.request.form["server_owner"]).fetchall()[0][5]
                    start_command = sqlquery("SELECT * FROM images WHERE id = ?", flask.request.form["server_image"],).fetchall()[0][2]
                    image = sqlquery("SELECT * FROM images WHERE id = ?", flask.request.form["server_image"],).fetchall()[0][3]
                    node_ip = sqlquery("SELECT * FROM nodes WHERE id = ?", flask.request.form["server_node"],).fetchall()[0][2]
                    node_api = sqlquery("SELECT * FROM nodes WHERE id = ?", flask.request.form["server_node"],).fetchall()[0][5]
                    uuid = os.urandom(10).hex()
                    payload = {
                        "api_key":  node_api,
                        "owner_api": owner_api,
                        "startup_command": start_command,
                        "image": image
                    }
                    try:
                        if requests.post("http://{}:8080/api/servers/{}/create".format(node_ip, uuid), data=payload).text == "server created":
                            sqlquery (
                                "INSERT INTO servers (name, ownerid, nodeid, memory, disk, uuid, owneremail, start_command, image, nodeip) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                flask.request.form["server_name"],
                                flask.request.form["server_owner"],
                                flask.request.form["server_node"],
                                flask.request.form["server_memory"],
                                flask.request.form["server_storage"],
                                uuid,
                                owner_email,
                                start_command,
                                image,
                                node_ip
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

# /api/admin/images/<imageid>/update

# csrf_token
# api_key

# image_name
# docker_image
# startup_command

# /api/admin/images/<imageid>/variables/create

# csrf_token
# api_key

# variable_name
# variable
