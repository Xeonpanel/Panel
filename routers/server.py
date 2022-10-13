
import flask, requests, json

from __main__ import app, query

@app.get("/dashboard/server/<serverid>")
def server(serverid):
    if flask.session:
        if len(query("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            data = query("SELECT * FROM servers WHERE id = ?", serverid)[0]
            imageid = data[6]
            startup = data[10]
            if len(query("SELECT * FROM server_variables WHERE server_id = ?", serverid)):
                variables = []
                for variable in query("SELECT * FROM image_variables WHERE image_id = ?", imageid):
                    variables.append(variable[2])
                if any(x in startup for x in variables):
                    for variable in variables:
                        variableid = query("SELECT * FROM image_variables WHERE image_id = ? and variable = ?", imageid, variable)[0][0]
                        if len(query("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)):
                            startup = startup.replace("[[{}]]".format(variable), query("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)[0][1])
                        else:
                            startup = startup.replace("[[{}]]".format(variable), "")
            return flask.render_template("/server/server.html", title="Console", query=query, serverid=serverid, startup=startup)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.get("/dashboard/server/<serverid>/files")
@app.get("/dashboard/server/<serverid>/files/<path:dir>")
def server_files(serverid, **dir):
    if flask.session:
        if len(query("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            if dir:
                subpath = dir["dir"]
                path = "/home/container/{}".format(dir["dir"])
            else:
                subpath = "/"
                path = "/home/container"
            return flask.render_template("/server/files.html", title="File Manager", query=query, serverid=serverid, json=json, path=path, subpath=subpath)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.get("/dashboard/server/<serverid>/configuration")
def server_configuration(serverid):
    if flask.session:
        if len(query("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            data = query("SELECT * FROM servers WHERE id = ?", serverid)[0]
            imageid = data[6]
            startup = data[10]
            if len(query("SELECT * FROM server_variables WHERE server_id = ?", serverid)):
                variables = []
                for variable in query("SELECT * FROM image_variables WHERE image_id = ?", imageid):
                    variables.append(variable[2])
                if any(x in startup for x in variables):
                    for variable in variables:
                        variableid = query("SELECT * FROM image_variables WHERE image_id = ? and variable = ?", imageid, variable)[0][0]
                        if len(query("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)):
                            startup = startup.replace("[[{}]]".format(variable), query("SELECT * FROM server_variables WHERE server_id = ? and image_id = ? and variable_id = ?", serverid, imageid, variableid)[0][1])
                        else:
                            startup = startup.replace("[[{}]]".format(variable), "")
            return flask.render_template("/server/configuration.html", title="Configuration", query=query, serverid=serverid, startup=startup)
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")

@app.get("/dashboard/server/<serverid>/files/edit/<path:dir>")
def edit_file(serverid, **dir):
    if flask.session:
        if len(query("SELECT * FROM servers WHERE owner_id = ? and id = ?", flask.session["id"], serverid)):
            payload = {
                "user_token": flask.session["token"],
                "file": dir["dir"]
            }
            file = requests.get("https://{}:8080/api/servers/{}/files/edit".format(query("SELECT * FROM nodes WHERE id = ?", query("SELECT * FROM servers WHERE id = ?", serverid)[0][5])[0][4], query("SELECT * FROM servers WHERE id = ?", serverid)[0][9]), data=payload).text
            return flask.render_template("/server/editfile.html", title="Edit File", query=query, content=file, serverid=serverid, path=dir["dir"])
        else:
            flask.abort(401)
    else:
        return flask.redirect("/login")