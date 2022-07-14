# Verify that user wants to install
echo "This script will install the following packages:"
# Check if user is root
if [ "$(id -u)" != "0" ]; then
   printf "This script must be run as root\nYou can login as root with\033[0;32m sudo su - " 1>&2
   exit 1
fi
read -p "Are you sure you want to continue? [y/n] " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
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
