const express = require("express");
const bcrypt = require("bcrypt");
const { User } = require("../models");
const { Op } = require("sequelize");

const router = express.Router();

router.get("/login", async (req, res) => {
    return res.render("auth/login", {message: req.flash("message")});
});

router.get("/register", async (req, res) => {
    return res.render("auth/register", {message: req.flash("message")});
});

router.get("/logout", async (req, res) => {
    req.session.destroy();
    return res.redirect("/");
});

router.post("/register", async (req, res) => {
    const { email, username,  password } = req.body;
    if (!email || !password || !username) {
        req.flash("message", "Credentials not provided");
        return res.render("auth/register", {message: req.flash("message")});
    }

    let user = await User.findOne({ where: { [Op.or]: [{ email: email }, { username: username }] } });
    if (user) {
        req.flash("message", "Username or email already taken");
        return res.render("auth/register", {message: req.flash("message")});
    }

    let salt = await bcrypt.genSalt(10);
    let hashed_password = await bcrypt.hash(password, salt);
    user = await User.create({ email: email, password: hashed_password, username: username });
    req.session.user = user;
    return res.redirect("/dashboard");
});

router.post("/login", async (req, res) => {
    const { username_email, password } = req.body;
    if (!username_email || !password) {
        req.flash("message", "Credentials not provided");
        return res.render("auth/login", {message: req.flash("message")});
    }

    let user = await User.findOne({ where: { [Op.or]: [{ email: username_email }, { username: username_email }] } });
    if (user) {
        if (await bcrypt.compare(password, user.password)) {
            req.session.user = user;
            return res.redirect("/dashboard");
        }
    }

    req.flash("message", "Invalid credentials");
    return res.render("auth/login", {message: req.flash("message")});
});

module.exports = router;