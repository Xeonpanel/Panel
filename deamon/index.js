const express = require("express");
const parser = require("body-parser");
const session = require("express-session");
const selfsigned = require("selfsigned");
const flash = require("connect-flash");
const crypto = require("crypto");
const chalk = require("chalk");
const https = require("https");
const path = require("path");
const os = require("os")
const fs = require("fs");
const { Token } = require("./models");

Token.findAll().then((token) => {
    if (token.length <= 0) {
        console.log(`[${chalk.red("Error")}] Token not found, please run the setup.js script`);
        process.exit(1);
    }
});

if (!fs.existsSync("./ssl/key.pem") || !fs.existsSync("./ssl/cert.pem")) {
    console.log(`[${chalk.red("Error")}] SSL certificate not found`);
    console.log(`[${chalk.yellow("Warn")}] Generating SSL certificate`);

    const attrs = [{ name: "commonName", value: os.hostname() }];
    const pems = selfsigned.generate(attrs, { days: 365 });

    try {
    fs.mkdirSync(path.join(__dirname, "ssl"));
    } catch (err) {}

    fs.writeFileSync(path.join(__dirname, "ssl", "key.pem"), pems.private);
    fs.writeFileSync(path.join(__dirname, "ssl", "cert.pem"), pems.cert);
    console.log(`[${chalk.green("Success")}] SSL certificate generated`);
}

const app = express();
app.use(session({
    secret: crypto.randomBytes(24).toString("hex"),
    resave: true,
    saveUninitialized: true,
}));
app.use(parser.urlencoded({ extended: false }));
app.use(parser.json());

app.use("/api", require("./api"));      

https.createServer({
    key: fs.readFileSync("./ssl/key.pem"),
    cert: fs.readFileSync("./ssl/cert.pem"),
}, app).listen(8080, () => {
    console.log(`[${chalk.cyan("Info")}] Using SSL certificate from ${path.join(__dirname, "ssl", "cert.pem")}`);
    console.log(`[${chalk.green("Success")}] Deamon started on https://localhost:8080`);
});