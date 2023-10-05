const checkAuth = require("./middleware/checkAuth");
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


if (!fs.existsSync("./ssl/key.pem") || !fs.existsSync("./ssl/cert.pem")) {
    console.log(`[${chalk.red("Error")}] SSL certificate not found`);
    console.log(`[${chalk.yellow("Warn")}] Generating SSL certificate`);

    const attrs = [{ name: "commonName", value: os.hostname() }];
    const pems = selfsigned.generate(attrs, { days: 90 });

    try {
    fs.mkdirSync(path.join(__dirname, "ssl"));
    } catch (err) {}

    fs.writeFileSync(path.join(__dirname, "ssl", "key.pem"), pems.private);
    fs.writeFileSync(path.join(__dirname, "ssl", "cert.pem"), pems.cert);
    console.log(`[${chalk.green("Success")}] SSL certificate generated`);
}

const app = express();
app.use(parser.urlencoded({ extended: false }));
app.use(parser.json());
app.use(session({
    // secret: crypto.randomBytes(24).toString("hex"),
    secret: "test",
    resave: true,
    saveUninitialized: true,
}));
app.use(flash());

app.set("views", __dirname + "/views");
app.set("view engine", "ejs");

app.get("/", checkAuth, async (req, res) => {
    return res.redirect("/dashboard");
});

app.use("/auth", require("./routes/auth"));      
app.use("/dashboard", require("./routes/dashboard"));
app.use("/admin", require("./routes/admin"));
app.use("/gateway", require("./routes/gateway"));

https.createServer({
    key: fs.readFileSync("./ssl/key.pem"),
    cert: fs.readFileSync("./ssl/cert.pem"),
}, app).listen(3000, () => {
    console.log(`[${chalk.cyan("Info")}] Using SSL certificate from ${path.join(__dirname, "ssl", "cert.pem")}`);
    console.log(`[${chalk.green("Success")}] Panel started on https://localhost:3000`);
});
