#!/bin/sh
# NOTICE: Requires chmod +x ./macosinit.sh

# CONFIG
SCHEDULE = false #OPTIONAL: Change to TRUE to schedule script to run every hour using crontab. Clear in future using crontab -r
ABSOLUTE_PATH_TO_SCRIPT = "~/Downloads/project_folder/twitterscraper.py" #REQUIRED: Change to absolute path of your python script.

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

python3 -m venv ./ # set up new venv for python installs, ~1 min
source bin/activate # activate venv
pip install playwright pandas  # ~60mb in total
playwright install # downloads chromium, firefox, webkit browsers ~unsure mb

#run python script right now
python3 twitterscraper.py
echo "Scheduled script every hour: $SCHEDULE\nSet up venv. Run script in future with $ python3 twitterscraper.py"