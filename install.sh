#!/bin/bash
echo "XeonPanel Installation Script"
echo "Copyright © 2022 Xeonpanel."
echo "Please join our community support discord server: https://discord.gg/4y9X28Ubxd"
echo ""
echo "Please note that this script is meant to be installed on a fresh OS. Installing it on a non-fresh OS may cause problems."
if [ "$(id -u)" != "0" ]; then
    printf "This script must be run as root\nYou can login as root with\033[0;32m sudo su -\033[0m\n" 1>&2
    exit 1
fi
echo "This script will install the following packages:"
read -p "Are you sure you want to continue? [y/n] " installation
if [[ $installation == "y" || $installation == "Y" || $installation == "yes" || $installation == "Yes" ]]
then
    echo "Installing..."
    apt update
    apt-get git python3 python3-pip -y
    cd /etc
    git clone https://github.com/Xeonpanel/Panel.git xeonpanel
    python3 -m pip install -r xeonpanel/requirements.txt
    mv /etc/xeonpanel/xeonpanel.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable --now xeonpanel.service
    echo "Panel succesfully installed and started.."
    echo "Now installing nginx config..."
    apt-get install nginx -y
	clear
    # ask if user wants to use domain or IP address
    echo "Do you want to use a domain name or an IP address?"
	echo ""
    echo "1. Domain name"
    echo "2. IP address"
    echo "3. Exit"
	echo ""
    read -p 'Enter your choice:'  choice
    if [[ $choice == "1" ]]
    then
        echo "Enter the domain name you want to use: "
        read domain
        cp /etc/xeonpanel/xeonpanel.conf /etc/nginx/sites-available/xeonpanel.conf
        sed -i "s/url/\n$domain\n/g" /etc/nginx/sites-available/xeonpanel.conf
        ln -s /etc/nginx/sites-available/xeonpanel.conf /etc/nginx/sites-enabled/xeonpanel.conf
        systemctl restart nginx
        echo "Panel is now available at http://$domain"
		read -p "Do you want to install deamon? [y/n] " -n 1 -r
		if [[ $REPLY == "y" || $REPLY == "Y" || $REPLY == "yes" || $REPLY == "Yes" ]]
		then
			apt update
			apt-get install git python3 python3-pip docker containerd docker.io -y
			python3 -m pip install flask flask_sock flask_cors docker waitress cryptography pyOpenSSL
			cd /etc
			git clone https://github.com/Xeonpanel/Deamon.git deamon
			mv /etc/deamon/deamon.service /etc/systemd/system/
			printf "Installation -->  Completed\n"
		else
			printf "Installation -->  Canceled\n"
		fi
	fi	
    if [[ $choice == "2" ]]
    then
        mv /etc/xeonpanel/xeonpanel.conf /etc/nginx/sites-available/xeonpanel.conf
        sed -i "s/url/\n_\n/g" /etc/nginx/sites-available/xeonpanel.conf
        ln -s /etc/nginx/sites-available/xeonpanel.conf /etc/nginx/sites-enabled/xeonpanel.conf
        systemctl restart nginx
        echo "Panel is now available"
		read -p "Do you want to install deamon? [y/n] " -n 1 -r
		if [[ $REPLY == "y" || $REPLY == "Y" || $REPLY == "yes" || $REPLY == "Yes" ]]
		then
			apt update
			apt-get install git python3 python3-pip docker containerd docker.io -y
			python3 -m pip install flask flask_sock flask_cors docker waitress cryptography pyOpenSSL
			cd /etc
			git clone https://github.com/Xeonpanel/Deamon.git deamon
			mv /etc/deamon/deamon.service /etc/systemd/system/
			printf "Installation -->  Completed\n"
		else
			printf "Installation -->  Canceled\n"
		fi
	fi
    if [[ $choice == "3" ]]
    then
        echo "Exiting..."
        exit 0
    else
        echo "Invalid option"
        exit
    fi
else
    echo "Installation cancelled."
fi
exit
