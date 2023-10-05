const checkAuth = require("../middleware/checkAuth");
var captcha = require("nodejs-captcha");
const express = require("express");
const crypto = require("crypto");

const router = express.Router();

router.get("/", checkAuth, async (req, res) => {
    return res.render("dashboard/index", {user: req.session.user, message: req.flash("message")});
});

router.get("/profile", checkAuth, async (req, res) => {
    return res.render("dashboard/profile", {user: req.session.user, message: req.flash("message")});
});

router.post("/profile/update", checkAuth, async (req, res) => {
    const { type } = req.params

    req.flash("message", "Not implemented yet");
    return res.redirect("/dashboard/profile");
});

module.exports = router;