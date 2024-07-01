from pathlib import Path
import re, string
from datetime import date, datetime
import ssl # required for bypassing nltk download ssl check
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------- Importing Data by iterating through data folder ---------- #
# Get list of all files in data/ directory
path = Path('./data')
data_files = list(path.iterdir())

# Convert to strings
for i in range(0, len(data_files)):
    data_files[i] = str(data_files[i])

# Read 
df = pd.read_csv(data_files[0])

for i in range (1, len(data_files)):
    if not data_files[i].endswith('.csv'): continue # skip if not .csv file
    else: df = pd.concat([df, pd.read_csv(data_files[i])])

# ---------- Data cleaning and pre-processing ---------- #
# about 20% duplicate rate
df = df.drop_duplicates()

# Data cleaning - convert date column to date_type object
df['raw_date'] = df['date']
df["hours"] = df["time"].apply(lambda time: time[0]+time[1]+":00")

# Combine raw_date and hours into single "date" column - Rowwise operation
df['date'] = df.apply(lambda row: f"{row['raw_date']} {row['hours']}", axis=1)

#### Language Processing: Init / Requirements
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt') # used for word-tokenization, PUNKT also comes with sentence tokenization
nltk.download('wordnet') # lexical db for english words - improved context
nltk.download('averaged_perceptron_tagger') # - contexual POS tagger algorithm
nltk.download('stopwords') # for removing filler words
nltk.download('vader_lexicon') # for Vader's sentiment analysis

#### Language Processing: Tokenization
# breaking tweets into discernable words 

# Function to clean noise
def remove_noise(tweet_tokens, stop_words = nltk.corpus.stopwords.words('english')):
    cleaned_tokens = []
    for token, tag in nltk.pos_tag(tweet_tokens):
        token = re.sub('[^A-Za-z0-9 ]+', '', token) # removes special characters except for ' ' (space)
        
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        
        lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

# Function which runs senitment analysis - Requires remove_noise() function
def sentiment_analysis(text):
    tokenized_text = word_tokenize(text) # based on nltk.tokenize.word_tokenizer() using PUNKT algorithm
    cleaned_tokenized_text = remove_noise(tokenized_text)
    cleaned_tokenized_text = ' '.join(cleaned_tokenized_text) # combine back into single string
    return cleaned_tokenized_text


# apply sentiment_analysis function to every row's 'post' column - saving it to 'tokenized_text' column
df['tokenized_text'] = df['post'].apply(sentiment_analysis) 


sid = SentimentIntensityAnalyzer() # create Vader sentiment analysis
# sentiment analysis using VADER
df['sentiment'] = df.apply(
    lambda row: sid.polarity_scores(row['tokenized_text'])['compound'], # get compound (overall) value from sentiment analysis
    axis = 1 # apply function rowise, not columnwise
)


# ---------- GRAPHING ---------- #

# Group by 'query' and 'date', and calculate mean and standard deviation for 'sentiment'
grouped = df.groupby(['query', 'date'])['sentiment'].agg(
    mean='mean',
    stdev='std'
).reset_index()

# Create the plot
plt.figure(figsize=(18, 10), dpi=150) 

# Loop through each query and plot
for query in grouped['query'].unique():
    query_data = grouped[grouped['query'] == query]
    plt.plot(query_data['date'], query_data['mean'], label=f'{query} Mean')
    plt.fill_between(query_data['date'], query_data['mean'] - query_data['stdev'], query_data['mean'] + query_data['stdev'], alpha=0.2)

# Customize the plot
plt.title('Sentiment Over Time by Topic')
plt.xlabel('Date Hour')
plt.xticks(rotation=-45, rotation_mode="anchor", ha="left", fontsize=8)

plt.ylabel('Mean Sentiment (Standard Deviation)')
plt.ylim(-1, 1)

plt.legend()
plt.grid(True)

plt.savefig('twittersentiment.png')

# SAVING CLEANED DF:

# Create data folder to house data if not exists:
Path("cleandata/").mkdir(parents=True, exist_ok=True)
DATE = date.today().strftime("%Y%m%d")
TIME = datetime.now().strftime("%H%M%S")
TIMESTAMP = str(DATE) + "_" + str(TIME)

#Save cleaned df
df.to_csv(f"cleandata/twitter_sentiment_{TIMESTAMP}.csv", index=False)