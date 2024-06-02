from pathlib import Path
from textblob import TextBlob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# about 20% duplicate rate
df = df.drop_duplicates()

# Data cleaning - convert date column to date_type object
df['raw_date'] = df['date']
df["hours"] = df["time"].apply(lambda time: time[0]+time[1]+":00")

# Combine raw_date and hours into single "date" column - Rowwise operation
df['date'] = df.apply(lambda row: f"{row['raw_date']} {row['hours']}", axis=1)

# Calculating sentiment using TextBlob
df["sentiment"] = df["post"].apply(lambda post: TextBlob(post).sentiment.polarity)

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

#Save cleaned df
df.to_csv('clean_twitterdata_sentiment.csv')