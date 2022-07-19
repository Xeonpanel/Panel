#!/bin/bash
echo "XeonPanel v0.8 Installation Script"
echo "Copyright © 2022 Xeonpanel."
echo "For support join our community: https://discord.gg/4y9X28Ubxd"
echo ""
if [ "$(id -u)" != "0" ]; then
    printf "This script must be run as root\nYou can login as root with\033[0;32m sudo su -\033[0m\n" 1>&2
    exit 1
fi
echo "This script will install the following packages:"
read -p "Are you sure you want to continue? [y/n] " installation
if [[ $installation == "y" || $installation == "Y" || $installation == "yes" || $installation == "Yes" ]]
then
    echo "Installing panel ( v0.8 )"
    apt update
    apt-get git python3 python3-pip certbot nginx -y
    cd /etc
    git clone https://github.com/Xeonpanel/Panel.git xeonpanel
    python3 -m pip install -r xeonpanel/requirements.txt
    mv /etc/xeonpanel/xeonpanel.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable --now xeonpanel.service
    echo "Installing nginx config..."
	clear
    read -p 'Enter your domain ( No IP ): ' domain
    read domain
    certbot certonly --standalone -d $domain
    mv /etc/xeonpanel/xeonpanel.conf /etc/nginx/sites-available/
    sed -i "s/url/\n$domain\n/g" /etc/nginx/sites-available/xeonpanel.conf
    ln -s /etc/nginx/sites-available/xeonpanel.conf /etc/nginx/sites-enabled/xeonpanel.conf
    systemctl restart nginx
    echo "Panel is now available at https://$domain"
    read -p "Do you want to install deamon? [y/n] " -n 1 -r
    if [[ $REPLY == "y" || $REPLY == "Y" || $REPLY == "yes" || $REPLY == "Yes" ]]
    then
        apt update
        apt-get install git python3 python3-pip docker containerd docker.io -y
        python3 -m pip install flask flask_sock flask_cors docker waitress 
        cd /etc
        git clone https://github.com/Xeonpanel/Deamon.git deamon
        mv /etc/deamon/deamon.service /etc/systemd/system/
        echo ""
        echo " --> Installation completed"
        echo ""
    else
        echo ""
        echo " --> Installation cancelled"
        echo ""
    fi
else
    echo ""
    echo " --> Installation cancelled"
    echo ""
fi
exit
