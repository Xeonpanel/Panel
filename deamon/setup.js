const { Token } = require("./models");
const args = require("minimist")(process.argv.slice(2));
const crypto = require("crypto");

Token.sync().then(() => {
    if (args.token.length <= 0) {
        console.log("Usage: node setup.js --token <token>");
        process.exit(1);
    }
    
    const token = args.token;
    
    Token.findAll().then((item) => {
        if (item.length > 0 && !args.force) {
            console.log("Token already initialized, use --force to override");
            process.exit(1);
        } else {
            if (args.force) {
                Token.destroy({ where: {} });
            }
            let randomKey = crypto.randomBytes(24).toString("hex");
            Token.create({
                public_key: Buffer.from(token, "base64").toString(),
                jwt_key: randomKey
            }).then(() => {
                console.log("Token initialized");
                process.exit(0);
            }).catch((err) => {
                console.log("Error creating token");
                console.log(err);
                process.exit(1);
            });
        }
    }).catch((err) => {
        console.log("Error checking token");
        console.log(err);
        process.exit(1);
    });
});

