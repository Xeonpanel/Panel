# Verify that user wants to install
echo "This script will install the following packages:"
# Are you sure you want to continue? [y/n]
read -p "Are you sure you want to continue? [y/n] " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo apt update
    sudo apt install git
    apt install python3
    apt install python3-pip
    python3 -m pip install flask
    python3 -m pip install requests
    git clone https://github.com/Xeonpanel/Panel.git
    mkdir -p /var/www/xeonpanel
    mv Panel/* /var/www/xeonpanel
    rm -rf Panel
    apt install screen
    screen
    cd /var/www/xeonpanel
    python3 app.py
else
    echo "Installation cancelled."
fi