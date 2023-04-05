#!/bin/bash

# Colors
RED='\033[0;31m' # Orange
GREEN='\033[0;32m' # Green
YELLOW='\033[1;33m' # Yellow
LCYAN='\033[1;36m' # Light Cyan
WHITE='\033[1;37m' # White
NC='\033[0m' # No Color

# Give execution permission to extraMetaPy.py and copy to /usr/bin
echo -e ${RED}[*] ${WHITE}Installing extraMetaPy 2.0...${NC}
pip install PySocks colorama googlesearch_python simplejson

# need the libimage-exiftool-perl
REQUIRED_PKG="libimage-exiftool-perl"
PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $REQUIRED_PKG|grep "install ok installed")
echo Checking for $REQUIRED_PKG: $PKG_OK
if [ "" = "$PKG_OK" ]; then
  echo "No $REQUIRED_PKG. Setting up $REQUIRED_PKG."
  sudo apt-get --yes install $REQUIRED_PKG
fi

chmod +x extraMetaPy.py
cp extraMetaPy.py /usr/bin/extraMetaPy
echo -e ${NC}
echo -e ${GREEN}[+] ${WHITE}Done!${NC}
echo -e

# Execute and display it
./extraMetaPy.py -h
