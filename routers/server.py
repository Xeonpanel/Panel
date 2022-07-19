import flask, requests, json

from __main__ import app, sqlquery

@app.route("/dashboard/server/<serverid>")
def server(serverid):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            data = sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0]
            imageid = data[6]
            startup = data[10]
            if len(sqlquery("SELECT * FROM server_variables WHERE server_id = ?", serverid)):
                variables = []
                for variable in sqlquery("SELECT * FROM image_variables WHERE image_id = ?", imageid):
                    variables.append(variable[2])
                if any(x in startup for x in variables):
                    for variable in variables:
                        variableid = sqlquery("SELECT * FROM image_variables WHERE image_id = ? and variable = ?", imageid, variable)[0][0]
                        if len(sqlquery("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)):
                            startup = startup.replace("[[{}]]".format(variable), sqlquery("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)[0][1])
                        else:
                            startup = startup.replace("[[{}]]".format(variable), "")
            return flask.render_template("/server/server.html", title="Console", sqlquery=sqlquery, serverid=serverid, startup=startup)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/dashboard/server/<serverid>/files")
@app.route("/dashboard/server/<serverid>/files/<path:dir>")
def server_files(serverid, **dir):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            if dir:
                payload = {
                    "user_token": flask.session["token"],
                    "path": dir["dir"]
                }
                subpath = dir["dir"]
                path = "/home/container/{}".format(dir["dir"])
                files = requests.get("https://{}:8080/api/servers/{}/files".format(sqlquery("SELECT * FROM nodes WHERE id = ?", sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0][5])[0][4], sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0][9]), data=payload).json()
            else:
                payload = {
                    "user_token": flask.session["token"],
                    "path": "/"
                }
                subpath = "/"
                path = "/home/container"
                files = requests.get("https://{}:8080/api/servers/{}/files".format(sqlquery("SELECT * FROM nodes WHERE id = ?", sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0][5])[0][4], sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0][9]), data=payload).json()
            return flask.render_template("/server/files.html", title="File Manager", sqlquery=sqlquery, serverid=serverid, json=json, files=files, path=path, subpath=subpath)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/dashboard/server/<serverid>/configuration")
def server_configuration(serverid):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            data = sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0]
            imageid = data[6]
            startup = data[10]
            if len(sqlquery("SELECT * FROM server_variables WHERE server_id = ?", serverid)):
                variables = []
                for variable in sqlquery("SELECT * FROM image_variables WHERE image_id = ?", imageid):
                    variables.append(variable[2])
                if any(x in startup for x in variables):
                    for variable in variables:
                        variableid = sqlquery("SELECT * FROM image_variables WHERE image_id = ? and variable = ?", imageid, variable)[0][0]
                        if len(sqlquery("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)):
                            startup = startup.replace("[[{}]]".format(variable), sqlquery("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)[0][1])
                        else:
                            startup = startup.replace("[[{}]]".format(variable), "")
            return flask.render_template("/server/configuration.html", title="Configuration", sqlquery=sqlquery, serverid=serverid, startup=startup)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.route("/dashboard/server/<serverid>/files/edit/<path:dir>")
def edit_file(serverid, **dir):
    if flask.session:
        if len(sqlquery("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            payload = {
                "user_token": flask.session["token"],
                "file": dir["dir"]
            }
            file = requests.get("https://{}:8080/api/servers/{}/files/edit".format(sqlquery("SELECT * FROM nodes WHERE id = ?", sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0][5])[0][4], sqlquery("SELECT * FROM servers WHERE id = ?", serverid)[0][9]), data=payload).text
            return flask.render_template("/server/editfile.html", title="Edit File", sqlquery=sqlquery, content=file, serverid=serverid, path=dir["dir"])
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")