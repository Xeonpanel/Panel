if [ "$(id -u)" != "0" ]; then
   printf "This script must be run as root\nYou can login as root with\033[0;32m sudo su -\033[0m\n" 1>&2
   exit 1
fi
echo "This script will install the following packages:"
read -p "Are you sure you want to continue? [y/n] " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
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
else
    echo "Installation cancelled."
fi
