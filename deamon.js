const express = require("express");
const fs = require("fs");
const https = require("https");

var port = 8000;

var options = {
    key: fs.readFileSync("./ssl/privatekey.pem"),
    cert: fs.readFileSync("./ssl/certificate.pem"),
};

var app = express();

var server = https.createServer(options, app).listen(port, function(){
  console.log("Express server listening on port " + port);
});

app.get("/", function (req, res) {
    res.writeHead(200);
    res.end("hello world\n");
});