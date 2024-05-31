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
plt.figure(figsize=(5, 4), dpi=150) 

# Loop through each query and plot
for query in grouped['query'].unique():
    query_data = grouped[grouped['query'] == query]
    plt.plot(query_data['date'], query_data['mean'], label=f'{query} Mean')
    plt.fill_between(query_data['date'], query_data['mean'] - query_data['stdev'], query_data['mean'] + query_data['stdev'], alpha=0.2)

# Customize the plot
plt.title('Sentiment Over Time by Topic')
plt.xlabel('Date Hour')
plt.xticks(rotation=20)
plt.ylabel('Mean Sentiment (Standard Deviation)')
plt.ylim(-1, 1)

plt.legend()
plt.grid(True)
plt.show()



df["sentiment", df['query'] == "artificialintelligence"] 

plt.boxplot(
    df[df['query'] == "artificialintelligence"]["sentiment"]
)

plt.boxplot(
    df[df['query'] == "politics"]["sentiment"]
)

plt.show()


# Create the plot
plt.figure(figsize=(14, 8))

# Loop through each query and plot
for query in grouped['query'].unique():
    query_data = grouped[grouped['query'] == query]
    plt.plot(query_data['date'], query_data['median'], label=f'{query} Median')
    plt.fill_between(query_data['date'], query_data['q1'], query_data['q3'], alpha=0.2)





print(pd.concat([df1, df2]))




df = pd.read_csv('twitter_scrape_20240529_215430.csv')



print(plt.boxplot(df["sentiment"]))

print(df["sentiment"])


# TODO next!
"""
> Need to add re-try if repeatedly getting failed reads.
> Because twitter limiting my browsing --> exhausted after 
"""