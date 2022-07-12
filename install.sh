# Verify that user wants to install
echo "This script will install the following packages:"
# Are you sure you want to continue? [y/n]
read -p "Are you sure you want to continue? [y/n] " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    sudo apt update
    sudo apt install git python3 python3-pip -y
    python3 -m pip install flask requests
    cd /var/www
    git clone https://github.com/Xeonpanel/Panel.git xeonpanel
    sudo mv /var/www/xeonpanel/xeonpanel.service /etc/systemd/system/
else
    echo "Installation cancelled."
fi
