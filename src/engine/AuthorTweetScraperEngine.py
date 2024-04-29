import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from src.utils.SeleniumUtils import getSoupFromDriver, navigateAndGetSoupFromDriver
from src.model.Tweet import Tweet
from src.utils.Utils import cleanText
import pandas as pd

DEFAULT_VALUE = "--"
TAGS_TEXT_SEPARATOR = " "

def loadAllTweers(driver, maxTweets):
    try:
        lastTweetsSize = 0
        while True:
            soup = getSoupFromDriver(driver)
            tweets = soup.findAll("div", {"class": re.compile('^mr-status-tweet')})
            if len(tweets)>=maxTweets:
                return tweets
            if lastTweetsSize == len(tweets):
                try:
                    moreButton = driver.find_element(By.XPATH,"//a[text()='Show More']")
                    moreButton.click()
                    time.sleep(4)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                except:
                    return tweets
            else:
                lastTweetsSize = len(tweets)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(4)
    except:
        return list()
    

def _getTweetDateAndLink(soup):
    try:
        link = soup.find('a', {'class': 'timeago'})
        return cleanText(link['datetime']), cleanText(link["href"])
    except:
        return DEFAULT_VALUE, DEFAULT_VALUE
    
def _getTweetText(soup):
    try:
        text = soup.find('div', {'class': 'mr-status-content'})
        return cleanText(text.getText(separator=TAGS_TEXT_SEPARATOR))
    except:
        return DEFAULT_VALUE, DEFAULT_VALUE
    
    
def scrapeAuthorsTweets(driver, authorLink, authorId, maxTweets):
    tweetsList = list()
    try:
        soup = navigateAndGetSoupFromDriver(driver, authorLink)
        allTweetTag = loadAllTweers(driver, maxTweets)

        for tweetTag in allTweetTag:
            tweet = Tweet()
            tweet.authorId = authorId
            date, link = _getTweetDateAndLink(tweetTag)
            tweet.date = date
            tweet.link = link
            tweet.text = _getTweetText(tweetTag)
            tweetsList.append(tweet)

        return tweetsList
    except:
        return tweetsList
