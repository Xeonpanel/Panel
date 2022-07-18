#!/bin/bash
if [ "$(id -u)" != "0" ]; then
    printf "This script must be run as root\nYou can login as root with\033[0;32m sudo su -\033[0m\n" 1>&2
    exit 1
fi
echo "This script will install the following packages:"
read -p "Are you sure you want to continue? [y/n] " installation
if [[ $installation =~ ^[Yy]$ ]]
then
    echo "Installing..."
    sudo apt update
    sudo apt install git python3 python3-pip -y
    cd /etc
    sudo git clone https://github.com/Xeonpanel/Panel.git xeonpanel
    python3 -m pip install -r xeonpanel/requirements.txt
    sudo mv /etc/xeonpanel/xeonpanel.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now xeonpanel.service
    echo "Panel succesfully installed and started.."
    echo "Now installing nginx config..."
    sudo apt install nginx -y
    # ask if user wants to use domain or IP address
    echo "Do you want to use a domain name or an IP address?"
    echo "1. Domain name"
    echo "2. IP address"
    echo "3. Exit"
    read -p 'Enter your choice:'  choice
    if [[ $choice =~ ^[1]$ ]]
    then
        echo "Enter the domain name you want to use: "
        read domain
        sudo cp /etc/xeonpanel/xeonpanel.conf /etc/nginx/sites-available/xeonpanel.conf
        sudo sed -i "s/url/\n$domain\n/g" /etc/nginx/sites-available/xeonpanel.conf
        sudo ln -s /etc/nginx/sites-available/xeonpanel.conf /etc/nginx/sites-enabled/xeonpanel.conf
        sudo systemctl restart nginx
        echo "Panel is now available at http://$domain"
    elif [[ $choice =~ ^[2]$ ]]
    then
        sudo mv /etc/xeonpanel/xeonpanel.conf /etc/nginx/sites-available/xeonpanel.conf
        sudo sed -i "s/url/\n_\n/g" /etc/nginx/sites-available/xeonpanel.conf
        sudo ln -s /etc/nginx/sites-available/xeonpanel.conf /etc/nginx/sites-enabled/xeonpanel.conf
        sudo systemctl restart nginx
        echo "Panel is now available"
    elif [[ $choice =~ ^[3]$ ]]
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
