# Twitter-scraper-python: a CS50x final project submission
#### Video URL: https://youtu.be/tjApwFCVDJY

## Twitter-scraper-python
A highly configurable TWITTER-SCRAPING BOT using Python library Playwright. Readily deployable inlocal environment, exports .csv data, and contains an NLP sentiment analysis pipeline compatible with distributedtwitterscraper.py.


## Project Introduction
This file structure houses all of the files I have been working on for the last month or so intended as the CS50x final project submission. As a data scientist with an interest in programmatic and automated ETL, analysis/modelling and visualisation data pipelines, I took CS50x as a way to fill any gaps of my programming knowledge. Having completed CS50x, I used the low-level “under-the-hood” understanding of memory to develop improved algorithms for my data analysis, which I have not fully considered or been fluent in prior. This knowledge and course will prove extremely valuable as my career progresses, and I take on more responsibility creating (hopefully) efficient and effective data pipelines. 

The primary purpose of this project was to develop a personal dataset for myself to learn natural language processing (NLP) and hone my machine learning algorithms/skills after struggling to find an adequate dataset on Kaggle. This project contains multiple scripts, mostly in python, which enables both the scraping and collection of twitter data in flatfile (.csv) format, but also contains a data processing and sentiment analysis script for automated data analysis and visualisation.


## INSTALLATION GUIDE
For MacOS or Linux users, the repository contains a macosinit.sh UNIX bash script to ease installation. There are numerous key steps required for successful installation.

### Requirements and Dependencies
The python scripts in this project were developed and tested on python version 3.10.3, ensure your machine has this or later python runtime installed. The macosinit.sh bash script assumes python is already installed.

Project package dependencies for all python scripts are listed in the requirements.txt. To correctly install all project dependencies, create a virtual environment in a terminal session, then run the following terminal command. These steps are automated in the macosinit.sh script.
`pip install -r requirements.txt`

Package Dependencies:
- numpy==1.26.4
- pandas==2.2.1
- matplotlib==3.8.3
- playwright==1.44.0
- nltk==3.8.1

Ensure after installing all packages, that Nightly Firefox is installed for playwright using the following command, executed in terminal:
`playwright install firefox`

### Script Configuration and Twitter Account Credentials
The twitterscraper.py must be configured prior to being run. To successfully configure twitterscraper.py, insert all relevant twitter account credential information into the script using a text editor or IDE, as well as tweaking any personal preference options in the top of the script in the “CONFIG:” section.

The distributedtwitterscraper.py file is more sophisticated, and allows distributed, multi-instance and automated scraping. It accepts up to 5 twitter account credentials by parsing a config.cfg with configparser. To manually create this file, view the [configparser docs](https://docs.python.org/3/library/configparser.html). Create a new section labelled 1-5 for every twitter account you would like to run, formatted as the following code block. These steps are automatically done using macosinit.sh via prompt/user input.
```
config.cfg
-------------
[1]
botusername = username
botpassword = password

[2]
botusername = username2
botpassword = password2
…
```

Note that in both scripts, no account credentials ever leave the working directory.
CAUTION: for security, after hard-coding the account details into twitterscraper.py, the file should never be shared or uploaded to GitHub.
CAUTION: for security, config.cfg should never be shared or uploaded to GitHub.

## USAGE GUIDE
If you used macosinit.sh to install project dependencies, this created a python virtual environment (venv) and installed package dependencies locally within the directory. This means executing either twitterscraper.py or distributedtwitterscraper.py from terminal will result in a “package not found” error. To solve this, ensure the venv is active from your terminal:
```
cd project/folder
source bin/activate 
```

### twitterscraper.py
After macosinit.sh or package installation and configuration, twitterscraper.py can be run from terminal:
`python twitterscraper.py`

### distributedtwitterscraper.py
After macosinit.sh or manual config.cfg creation, distributedtwitterscraper.py can be run using CLI or prompts. By default, if no CLI arguments are provided, distributedtwitterscraper.py will prompt user to enter the following parameters: search query, bot number (as per configparser section in config.cfg), headless mode for Nightly Firefox. Headless mode refers to No GUI, where the browser will execute without a visible interface. distributedtwitterscraper.py accepts these parameters as CLI, shown in the code snippet below, where:
`python distributedtwitterscraper.py query bot_number headless`
- query is a no-space string for querying
- bot_number is an int corresponding to config.cfg sections
- headless accepts a char, either y or n (y/n)

Entering any other CLI arguments, or the incorrect format will result in an early script termination.

This script takes approximately 10 minutes to complete. It was developed as a distributed script, so that multiple instances of the script using multiple twitter accounts can be run at once. To do so, it is recommended to execute the script using CLI arguments across multiple terminal instances.

### sentimentanalysis.py
This script is only compatible for running with distributedtwitterscraper.py. There is no installation requirement or execution specifications.

## Files and Purposes

### ./sample_data/
A directory containing a few smaller example .csv files showcasing the structure and format of extracted data using the developed extraction algorithm.

### requirements.txt
A simple text folder used to manage project package dependencies, as well as automate installation.

### macosinit.sh
A UNIX bash script for user-friendly config.cfg creation/configuration with twitter account details, virtual environment creation, and package dependencies installation (using requirements.txt).

### twitterscraper.py
This script was the preliminary playwright based twitter scraper developed, and therefore offers little advantage over its successor, distributedtwitterscraper.py. Using configurable, hard-coded global variables at the top of the script, it launches a playwright headless (or head-full) browser, navigates to twitter, and uses the hard-coded account credentials to sign in and extract usernames, text (posts) and timestamps of tweets. Developing this extraction algorithm was a time-consuming process; the html, css and javascript structure of twitter was dissected and hijacked to obtain post-level data. The data is then cleaned and organised using pandas, and exported to a .csv

### distributedtwitterscraper.py
This is the more sophisticated and advanced twitter scraper of the two scripts. Although the algorithm follows a similar structure, it presents numerous advantages and features over its predecessor:
- increased extraction efficiency: fewer duplicate posts and redundancies at shorter running time
- decreased memory usage: more frequent query+time-stamped .csv exports to isolated ./data/ directory
- accepts and sanitises CLI inputs for script automation
- uses config.cfg along with configparser to allow distributed execution: multiple accounts and multiple instances
- config.cfg usage separates hard-coded account credentials, decreases security risk
It iterates through a ./data/ directory and combines all outputted .csv files from distributedtwitterscraper.py

### sentimentanalysis.py
The primary purpose of this project was to practice and develop my NLP and machine learning skills + algorithms. The idea for a sentiment analysis was inspired by the following article, “[How to perform sentiment analysis in python using the natural language tool kit](https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk)”  where much of the flow and structure of sentimentanalysis.py is based on.

The begins by using the pathlib to obtain a list of all the files in the ./data/ directory (sourced from distributedtwitterscraper.py), and then iteratively appends them to a pandas dataframe if they are .csv files. The usual data cleaning steps such as: datatype conversion, duplication dropping and date formatting follow thereafter. An unverified SSL certificate is created to bypass http-connection problems when attempting to download the required natural language toolkit (NLTK) tools. These tools are used in a custom cleaning function, which rowise (iteratively) takes the string post content, sanitises any special characters, tokenizes the text, normalizes the tokens by lemmatization, contextually tags each token, and removes any filler/stop words. These tokens are then re-combined as a cleaned string version of the original post, and stored as a new column in the pandas dataframe. Finally, a sentiment analysis using a pre-trained model is done iteratively, and the overall sentiment of the cleaned post content (sanitised, tokenised, normalised) is saved as a new column on the dataframe. The pre-trained model is the [VADER model](https://www.nltk.org/_modules/nltk/sentiment/vader.html), which has been trained on social media content and is an ideal use-case model for this script. 

Using matplotlib, the sentiment of each post is plotted along with the timestamp (by date and hour), further stratified by which query/topic the post was found using. Finally the cleaned and processed sentiment dataframe is saved as a .csv in the ./cleandata/ directory.

## Design choices / discussion
Modularised scripts: the initial twitter scraper script, twitterscraper.py was kept as an alternative option to requiring the config.cfg. Separating distributedtwitterscraper.py and sentimentanalysis.py improves the re-usability and versatility of the scripts. Primarily this allows you to run the sentiment analysis on an as-needed basis whilst collecting data. 

Installation automation with macosinit.sh: As I was porting these scripts from/to github, I found the need to re-insert my twitter account credentials quite tedious, and thought it would be a better design choice to automate the set up with no prior knowledge of configparser (instead using prompts).

Twitter account credential management: in the initial twitterscraper.py script, hard-coding the account credentials was my first choice due to simplicity. As the installation and script became more sophisticated, I decided it would be more secure, and more user-friendly to migrate the credentials from an in-script to an outscript. This also acted to protect myself when uploading my scripts to GitHub.

Extraction data algorithm: As with arguably all coding projects, my algorithm to extract the data using playwright demanded a lot of trial and error along with benchmarking. One of the most important design choices in this algorithm was the method of reverse-engineering the web page to obtain each post’s html content. This process took a lot of manual debugging and investigation of the webpage, where I ultimately identified numerous css classes by which I could obtain post elements containing the necessary contents such as username, post text (tweet), and timestamp. Other implementation details such as the anti-bot delays I hardcoded were subject to much benchmarking, where percentage error was recorded against time taken to find a balance where one script could generate ~50 unique posts a minute.

Flatfile data storage and organization: Storing scraped data in .csv files was a difficult decision. As I work with AWS, I was considering hosting the scripts on AWS Lambda, and saving the data to a database (DynamoDB or RDS) or instead an object store (S3). However, I chose to prioritise cost, as I was unsure what size data I would require for my modelling. Flatfiles were also chosen, seeing as they are the primary storage type for large data stores, and integrate very easily with multiple tools, thus making my scripts more malleable. 

Sentiment analysis: according to my research, NLTK was/is one of the most popular NLP libraries available in python, with proficient documentation and community. Following on from the article which I linked earlier, I believed this library would sufficiently enable me to conduct the data processing steps (sanitsation, tokenisation, contextual tagging) and sentiment analysis. Originally I had used TextBlob’s pre-trained sentiment analysis model, however after reading numerous articles and documentation I saw VADER was the improved successor, and decided to use VADER to generate the sentiment values.
