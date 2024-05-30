#!/bin/sh
# NOTICE: Requires chmod +x ./macosinit.sh

# Requesting if want schedule
echo "Welcome to twitterscraper.py setup. Do you wish to schedule the script for hourly run? You can remove stop it by removing it from crontab at any time with $ crontab -r. (y/n)"
read SCHEDULE

while [ $SCHEDULE != "y" ] && [ $SCHEDULE != "n" ]; do
    echo "Only 'y' or 'n' are accepted responses. Please try again."
    read user_number
done

if [ $SCHEDULE == "y" ]; then
    SCHEDULE=true
else
    SCHEDULE=false
fi

# Requesting file path
echo "Schedule = $SCHEDULE. Please provide the absolute file path of the twitterscraper.py file. This can be done from Finder on MacOS:"
read ABSOLUTE_PATH_TO_SCRIPT

while [ ABSOLUTE_PATH_TO_SCRIPT == "" ]; do
    echo "Please provide non-empty value."
    read ABSOLUTE_PATH_TO_SCRIPT
done

# Schedule cron job
if $SCHEDULE; then
    # Create cron job
    new_cron_job="0 1 * * * python3 $ABSOLUTE_PATH_TO_SCRIPT"  # run every hour, at the 0th minute, every day/month/year

    # Run process to return any cron jobs for "twitterscraper"
    crontab -l | grep twitterscraper.py

    # previous process $? will exit with 0 if something is found
    if [ $? -eq 0 ]; then 
        echo "Cron job already exists. No changes made."
    else
        # Get current crontab entries
        crontab -l > mycron

        # Add new cron job to the file
        echo "$new_cron_job" >> mycron

        # Install the new crontab
        crontab mycron

        # Clean up
        rm mycron

        echo "New cron job added successfully."
    fi
fi

# setting up dependencies
echo "Setting up python virtual environment and downloading Python requirements: playwright (dep: Nightly firefox) and pandas."
python3 -m venv ./ # set up new venv for python installs, ~1 min
source bin/activate # activate venv
pip install playwright pandas  # ~60mb in total
playwright install firefox # downloads only firefox ~85mb


# Requesting if want run script now
echo "Setup complete. Do you want to run the python script now? (y\n)"
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

echo "Setup completed. Run script manually with $ python3 twitterscraper.py"