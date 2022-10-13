import flask, hashlib, sys, time, requests, os

from __main__ import app, query

@app.post("/api/password/<userid>/update")
def api_update_password(userid):
    if flask.session:
        if flask.request.form.get("csrf_token") == flask.session["csrf_token"]:
            data = query(
                "SELECT * FROM users WHERE password = ? and id = ?",
                hashlib.sha256(
                    flask.request.form.get("password").encode("utf-8")
                ).hexdigest(),
                userid
            )
            if len(data):
                query(
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

@app.post("/api/username/<userid>/update")
def api_update_username(userid):
    if flask.session:
        if flask.request.form.get("csrf_token") == flask.session["csrf_token"]:
            data = query(
                "SELECT * FROM users WHERE password = ? and id = ?",
                hashlib.sha256(
                    flask.request.form.get("password").encode("utf-8")
                ).hexdigest(),
                userid
            )
            if len(data):
                query(
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

@app.post("/api/admin/settings/update")
def api_update_settings():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    query("UPDATE settings SET panel_name = ?", flask.request.form.get("panel_name"),)
                    query("UPDATE settings SET panel_logo = ?", flask.request.form["panel_logo"],)
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

@app.post("/api/admin/reboot")
def api_reboot_server():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    if data[0][0] == 1:
                        time.sleep(3)
                        os.execv(sys.executable, ["python"] + sys.argv)
                    else:
                        flask.flash("Only the master user can restart the panel", "error")
                        return flask.redirect("/admin")
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin")
            else:
                flask.abort(401)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.post("/api/admin/reset")
def api_factory_reset():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    if data[0][0] == 1:
                        os.remove("database.db")
                        os.execv(sys.executable, ["python"] + sys.argv)
                    else:
                        flask.flash("Only the master user can reset the panel", "error")
                        return flask.redirect("/admin")
                else:
                    flask.flash("Something went wrong", "error")
                    return flask.redirect("/admin")
            else:
                flask.abort(401)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.post("/api/admin/nodes/create")
def api_create_node():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    query(
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

@app.post("/api/admin/users/create")
def api_create_user():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    if len(query("SELECT * FROM users WHERE name = ? or email = ?", flask.request.form.get("username"), flask.request.form.get("email"))):
                        flask.flash("User already exists", "error")
                        return flask.redirect("/admin/users")
                    else:
                        query( 
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

@app.post("/api/admin/users/<userid>/update")
def api_update_user(userid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form["token"])
            if len(data):
                if data[0][5] == "administrator":
                    if len(query("SELECT * FROM users WHERE id = ?", userid)):
                        if int(userid) == 1:
                            flask.flash("Cannot update master user", "error")
                            return flask.redirect("/admin/users")
                        else:
                            if flask.request.form.get("password"):
                                query(
                                    "UPDATE users SET name = ?, email = ?, password = ?, user_type = ? WHERE id = ?",
                                    flask.request.form.get("username"),
                                    flask.request.form.get("email"),
                                    flask.request.form.get("password"),
                                    flask.request.form.get("user_type"),
                                    userid
                                )
                            else:
                                query(
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

@app.post("/api/admin/images/create")
def api_create_image():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    query(
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

@app.post("/api/admin/servers/create")
def api_create_server():
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    if len(query("SELECT * FROM servers WHERE ip_port = ?", "{}:{}".format(query("SELECT * FROM nodes WHERE id = ?", flask.request.form.get("server_node"))[0][4], flask.request.form.get("server_port")))):
                        flask.flash("This port is already used", "error")
                        return flask.redirect("/admin/servers")
                    try:
                        server_uuid = os.urandom(13).hex()
                        payload = {
                            "system_token": query("SELECT * FROM nodes WHERE id = ?", flask.request.form.get("server_node"))[0][5],
                            "user_token": flask.request.form.get("token"),
                            "port": flask.request.form.get("server_port"),
                            "memory": flask.request.form.get("server_memory")
                        }
                        if requests.post("https://{}:8080/api/servers/{}/create".format(query("SELECT * FROM nodes WHERE id = ?", flask.request.form.get("server_node"))[0][4], server_uuid), data=payload).text == "server created":
                            query (
                                "INSERT INTO servers (name, memory, disk, ip_port, node_id, image_id, owner_id, suspended, uuid, image, startup) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                flask.request.form.get("server_name"),
                                flask.request.form.get("server_memory"),
                                flask.request.form.get("server_storage"),
                                "{}:{}".format(query("SELECT * FROM nodes WHERE id = ?", flask.request.form.get("server_node"))[0][4], flask.request.form.get("server_port")),
                                flask.request.form.get("server_node"),
                                flask.request.form.get("server_image"),
                                flask.request.form.get("server_owner"),
                                0,
                                server_uuid,
                                query("SELECT * FROM images WHERE id = ?", flask.request.form.get("server_image"))[0][3],
                                query("SELECT * FROM images WHERE id = ?", flask.request.form.get("server_image"))[0][2]
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

@app.post("/api/admin/images/<imageid>/update")
def api_update_image(imageid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    query(
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

@app.post("/api/admin/images/<imageid>/variables/create")
def api_create_variable(imageid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    query(
                        "INSERT INTO image_variables (name, variable, image_id) VALUES (?, ?, ?)",
                        flask.request.form.get("variable_name"),
                        flask.request.form.get("variable"),
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

@app.post("/api/admin/images/<imageid>/variables/<variableid>/update")
def api_update_variable(imageid, variableid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    query(
                        "UPDATE image_variables SET name = ?, variable = ? WHERE id = ?",
                        flask.request.form.get("variable_name"),
                        flask.request.form.get("variable"),
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

@app.post("/api/admin/images/<imageid>/variables/<variableid>/delete")
def api_delete_variable(imageid, variableid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM users WHERE token = ?", flask.request.form.get("token"))
            if len(data):
                if data[0][5] == "administrator":
                    query("DELETE FROM image_variables WHERE id = ? and image_id = ?", variableid, imageid)
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

@app.post("/api/servers/<serverid>/variables/update")
def api_update_server_variable(serverid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM servers WHERE id = ? and owner_id = ?", serverid, flask.session["id"])
            if len(data):
                if len(query("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, flask.request.form.get("image_id"), flask.request.form.get("variable_id"))):
                    query("UPDATE server_variables SET data = ? WHERE server_id = ? and image_id = ? and variable_id = ?", flask.request.form.get("variable_data"), serverid, flask.request.form.get("image_id"), flask.request.form.get("variable_id"))
                    return flask.redirect("/dashboard/server/{}/configuration".format(serverid))
                else:
                    query("INSERT INTO server_variables (data, image_id, server_id, variable_id) VALUES (?, ?, ?, ?)", flask.request.form.get("variable_data"), flask.request.form.get("image_id"), serverid, flask.request.form.get("variable_id"))
                    return flask.redirect("/dashboard/server/{}/configuration".format(serverid))
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.post("/api/servers/<serverid>/reinstall")
def api_reinstall_server(serverid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM servers WHERE id = ? and owner_id = ?", serverid, flask.session["id"])
            if len(data):
                startup_command = query("SELECT * FROM images WHERE id = ?", flask.request.form.get("server_image"))[0][2]
                docker_image = query("SELECT * FROM images WHERE id = ?", flask.request.form.get("server_image"))[0][3]
                imageid = query("SELECT * FROM servers WHERE id = ?", serverid)[0][6]
                query("DELETE FROM server_variables WHERE image_id = ? and server_id = ?", imageid, serverid)
                query("UPDATE servers SET image_id = ?, startup = ?, image = ? WHERE id = ?", flask.request.form.get("server_image"), startup_command, docker_image, serverid)
                flask.flash("Server reinstall completed succesfully", "succes")
                return flask.redirect("/dashboard/server/{}/configuration".format(serverid))
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.post("/api/servers/<serverid>/rename")
def api_rename_server(serverid):
    if flask.session:
        if flask.session["csrf_token"] == flask.request.form.get("csrf_token"):
            data = query("SELECT * FROM servers WHERE id = ? and owner_id = ?", serverid, flask.session["id"])
            if len(data):
                query("UPDATE servers SET name = ? WHERE id = ?", flask.request.form.get("server_name"), serverid)
                flask.flash("Server name changed succesfully", "succes")
                return flask.redirect("/dashboard/server/{}/configuration".format(serverid))
            else:
                flask.abort(404)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")
