#!/bin/sh
# NOTICE: Requires chmod +x ./macosinit.sh

# Requesting if want schedule
echo "Welcome to twitterscraper.py setup.\n\n"

# writing config to config.cfg
echo "twitterscraper.py requires a twitter account username and password to scrape data. If you do not provide these now, you must manually create and enter them in a config.cfg later."
echo "Do you wish to provide these now? (y/n)\n"

read BOT_NOW

COUNT=1
while [ $BOT_NOW != "y" ] && [ $BOT_NOW != "n" ]; do
    echo "Only 'y' or 'n' are accepted responses. Please try again."
    read BOT_NOW
done

if [ $BOT_NOW == "y" ]; then
    echo "\nPlease provide the twitter bot username. Ensure this is correct, there will be no re-try."
    read BOT_USERNAME
    
    echo "\nPlease provide the twitter bot password. Ensure this is correct, there will be no re-try."
    read BOT_PASSWORD
    
    echo "\nWriting details to config.cfg\n"
    echo "[$COUNT]" > config.cfg
    COUNT=$((COUNT+1)) # increment count by 1
    echo "botusername = $BOT_USERNAME" >> config.cfg
    echo "botpassword = $BOT_PASSWORD" >> config.cfg
fi

echo "Do you wish to set up multiple bots now in order to use distributedtwitterscraper.py (y/n)?"
read MULTI
while [ $MULTI != "y" ] && [ $MULTI != "n" ]; do
    echo "Only 'y' or 'n' are accepted responses. Please try again."
    read MULTI
done

if [ $MULTI == "y" ]; then
    MULTI=true
else
    MULTI=false
fi

while $MULTI; do
    echo "\nPlease provide the twitter bot username. Ensure this is correct, there will be no re-try."
    read BOT_USERNAME
    
    echo "\nPlease provide the twitter bot password. Ensure this is correct, there will be no re-try."
    read BOT_PASSWORD
    
    echo "\nWriting details to config.cfg\n"
    echo "[$COUNT]" > config.cfg
    COUNT=$((COUNT+1)) # increment count by 1
    echo "botusername = $BOT_USERNAME" >> config.cfg
    echo "botpassword = $BOT_PASSWORD" >> config.cfg
    
    echo "Bot added to config.cfg - do you wish to create another? (y/n) "
    read MULTI
    while [ $MULTI != "y" ] && [ $MULTI != "n" ]; do
        echo "Only 'y' or 'n' are accepted responses. Please try again."
        read MULTI
    done

    if [ $MULTI == "y" ]; then
        MULTI=true
    else
        MULTI=false
    fi
done

# setting up dependencies
echo "Setting up python virtual environment and downloading Python requirements: playwright (dep: Nightly firefox) and pandas."
python3 -m venv ./ # set up new venv for python installs, ~1 min
source bin/activate # activate venv
pip install playwright pandas  # ~60mb in total
playwright install firefox # downloads only firefox ~85mb


# Requesting if want run script now
echo "\n\nSetup complete. Do you want to run the python script now? (y\n)"
read LAUNCH

while [ $LAUNCH != "y" ] && [ $LAUNCH != "n" ]; do
    echo "Only 'y' or 'n' are accepted responses. Please try again."
    read LAUNCH
done

if [ $LAUNCH == "y" ]; then
    LAUNCH=true
else
    LAUNCH=false
fi

if $LAUNCH; then
    python3 twitterscraper.py
fi

echo "Setup completed. Run script manually with $ python3 twitterscraper.py while in venv."