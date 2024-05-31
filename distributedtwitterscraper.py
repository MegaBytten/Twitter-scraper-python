# # # # # # Info and Setup # # # # # #
# Only accepts posts in ENGLISH ("en"). No input sanitsation --> do not directly load into DBs
# 3 queries, 100 batches generates 3x .csvs of ~ 1500 unique posts in 30m
# > =~ 50 unique posts / min
# > highly contingent on how active your topics (queries) are, if slow-posting inactive searches then more redundant duplicates which are removed

# Dependencies and installation already handled in macosinit.sh
# Inlcuding twitter bot account username/password into config.cfg

# Running script
# $ source bin/activate
# MacOS: $ python3 twitterscraper.py
# # # # # # # # #  # # # # # # # # # #


# # # # IMPORTS: DO NOT CHANGE # # # #
from datetime import date, datetime
from pathlib import Path
import configparser

import pandas as pd
from playwright.sync_api import sync_playwright # sync_playwright is actually a function, returns contxt manager


# Start clock for runtime assessment
startTime = datetime.now()
# # # # # # # # #  # # # # # # # # # #


# # # #  CONFIG: MUST CHANGE  # # # #
# Playwright has headless = True by default, meaning no UI on browser.
HEADLESS = False

# Number of iterations of posts. Each batch takes approximately 6s to run, generates ~ 5 unique posts
BATCHES = 80
# # # # # # # # #  # # # # # # # # # #


# # # # # #  SCRIPT  # # # # #
# GLOBAL DATA VARS
QUERY = input("Enter URL-encoded search query: ")
BOT_NUM = input("Which bot # would you like to use (see config.cfg) (1-5): ")
usernames, post_content, times, dates = [], [], [], []

# Bot username and password already taken from config.cfg - do not change here.
BOT_X_USERNAME = ""
BOT_X_PSWD = ""

# Function checks if all required config / dependencies are ready
def initChecks():
  global BOT_X_USERNAME, BOT_X_PSWD
  
  # CHECK IF CONFIG FILE EXISTS
  if not Path("config.cfg").is_file():
      exit("config.cfg not found.")

  # Read BOT_USERNAME and BOT_PASSWORD from config.cfg
  config = configparser.RawConfigParser()
  config.read("config.cfg")

  if not config.has_section(BOT_NUM):
    exit(f"{BOT_NUM} section in config.cfg not found")

  if not config.has_option(BOT_NUM, "botusername") or not config.has_option(BOT_NUM, "botpassword"):
    exit("X Bot username/password not provided")
      
  BOT_X_USERNAME = config.get(BOT_NUM, "botusername")
  BOT_X_PSWD = config.get(BOT_NUM, "botpassword")
  
  # Create data folder to house data if not exists:
  Path("data/").mkdir(parents=True, exist_ok=True)

def main():
  global usernames, post_content, times, dates

  with sync_playwright() as p:
    
    # Launch browser, with either headless or UI enabled
    browser = p.firefox.launch(headless=HEADLESS)
    
    # iterates through queries
    print(f"Starting Query: {QUERY}")
    # reset all lists, as previous data written to .csv
    usernames, post_content, times, dates = [], [], [], []
    
    #Navigate to X and sign in
    page = browser.new_page()
    page.goto(f'https://x.com/search?q={QUERY}&f=live')
    page.wait_for_timeout(2000) # wait 1s
    
    page.locator('input[name="text"]').fill(BOT_X_USERNAME)
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Next").click()

    page.wait_for_timeout(2000)
    
    page.locator('input[name="password"]').fill(BOT_X_PSWD)
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Log in").click()
    
    page.wait_for_timeout(7500) # wait 7.5 seconds for page to load
      
    # Add 10 batches posts
    for i in range(1, BATCHES):
        batch_add_posts(page)
        page.wait_for_timeout(1500) # 1.5s wait to refresh content between batch loads
      
    # Close page, and open new page for next query
    page.close()
    
    # Save data using Pandas to .csv
    df = pd.DataFrame(
    {'username': usernames,
    'time': times,
    'date': dates,
    'post': post_content,
    'query': QUERY
    })
    
    # remove duplicates
    df = df.drop_duplicates()
    
    DATE = date.today().strftime("%Y%m%d")
    TIME = datetime.now().strftime("%H%M%S")
    TIMESTAMP = str(DATE) + "_" + TIME
    df.to_csv(f"data/twitter_scrape_{QUERY}_{TIMESTAMP}.csv", index=False)
    print('\n')
    
    # Done with queries loop
    browser.close()


def batch_add_posts(page):
  # scroll 20 * 250 pixels to load new content
  NUMBER_SCROLLS = 20
  MOUSE_SCROLL_Y = 250
  for i in range(0,NUMBER_SCROLLS):
    page.mouse.wheel(0, MOUSE_SCROLL_Y)
    page.wait_for_timeout(100) # 10 ms - content load and reduce bot footprint
  
  # get total number of tweets available on loaded page
  new_posts = page.query_selector_all('article.css-175oi2r.r-18u37iz.r-1udh08x.r-1c4vpko.r-1c7gwzm.r-o7ynqc.r-6416eg.r-1ny4l3l.r-1loqt21')
  print("Posts added in this batch", len(new_posts))

  for i in range(0, len(new_posts)):
    
    # check if post exists:
    post_lang_check = new_posts[i].query_selector('div.css-146c3p1.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim')
    
    # Check if post is in english, if not skip
    if (post_lang_check):
      if (post_lang_check.get_attribute('lang') != "en"): continue
    
    
    username_element = new_posts[i].query_selector_all('a.css-175oi2r.r-1wbh5a2.r-dnmrzs.r-1ny4l3l.r-1loqt21')[1] # taking second hit, because first one is just account _name_ not _handle_
    post_text_element = new_posts[i].query_selector('div.css-146c3p1.r-8akbws.r-krxsd3.r-dnmrzs.r-1udh08x.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-16dba41.r-bnwqim')
    time_element = new_posts[i].query_selector('time')

    # Extract the content if the element exists
    if username_element:
      username = username_element.text_content()
    else: username = "No username found"
    
    if post_text_element:
      post_text = post_text_element.text_content()
    else: post_text = "No text found"
    
    if time_element:
      timedate = time_element.get_attribute('datetime')
      timedate = timedate[:-5] # remove last characters to get rid of ".000Z"
      timedate = timedate.split("T")
    else: timedate = ["No time found", "No date found"]
     # remove last 4 characters to get rid of weird JS formatted 000Z
    
    # Append to the lists
    usernames.append(username)
    post_content.append(post_text)
    dates.append(timedate[0])
    times.append(timedate[1])

if __name__ == '__main__':
  initChecks()
  main()
    
  time_taken = datetime.now() - startTime
  # Convert time_taken to total seconds
  total_seconds = int(time_taken.total_seconds())

  # Calculate hours, minutes, and seconds
  hours, remainder = divmod(total_seconds, 3600)
  minutes, seconds = divmod(remainder, 60)

  # Format the result
  formatted_time = f"{hours}h {minutes}m {seconds}s"
  print("Time taken:", formatted_time)
# # # # # #  SCRIPT  END  # # # # #