# Verify that user wants to install
echo "This script will install the following packages:"
# Are you sure you want to continue? [y/n]
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
    echo "\n\n Panel succesfully installed and started.. \n\n"
else
    echo "Installation cancelled."
fi
