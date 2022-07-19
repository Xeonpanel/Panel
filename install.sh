#!/bin/bash
clear
echo "XeonPanel v0.8 Installation Script"
echo "Copyright © 2022 Xeonpanel."
echo "For support join our community: https://discord.gg/4y9X28Ubxd"
sleep 1s
echo ""
if [ "$(id -u)" != "0" ]; then
    printf "This script must be run as root\nYou can login as root with\033[0;32m sudo su -\033[0m\n" 1>&2
    exit 1
fi
read -p "Are you sure you want to continue? [y/n] " installation
if [[ $installation == "y" || $installation == "Y" || $installation == "yes" || $installation == "Yes" ]]
then
    clear
    echo "Installing panel ( v0.8 )"
    echo ""
    sleep 1s
    sudo apt update
    sudo apt-get --ignore-missing install python3 git python3-pip nginx certbot python3-certbot-nginx
    cd /etc
    git clone https://github.com/Xeonpanel/Panel.git xeonpanel
    python3 -m pip install flask requests
    mv /etc/xeonpanel/xeonpanel.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable --now xeonpanel.service
    echo "Installing nginx config..."
	clear
    read -p 'Enter your domain ( No IP ): ' domain
    echo ""
    sudo certbot certonly --standalone -d $domain
    cp /etc/xeonpanel/xeonpanel.conf /etc/nginx/sites-available/xeonpanel.conf
    sed -i "s/url/$domain/" /etc/nginx/sites-available/xeonpanel.conf
    ln -s /etc/nginx/sites-available/xeonpanel.conf /etc/nginx/sites-enabled/xeonpanel.conf
    systemctl restart nginx
    echo "Panel is now available at https://$domain"
else
    echo ""
    echo " --> Installation cancelled"
    echo ""
fi
exit
