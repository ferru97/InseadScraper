import re
import time
from bs4 import BeautifulSoup
from email_validator import validate_email
from selenium.webdriver.common.by import By
from src.utils.SeleniumUtils import getSoupFromDriver, navigateAndGetSoupFromDriver
from urllib.parse import urlsplit, urlunsplit
from src.model.Author import Author
from src.utils.Utils import cleanText
import pandas as pd

DEFAULT_VALUE = "--"
TAGS_TEXT_SEPARATOR = " "

def _getAuthorName(soup):
    try:
        nameTag = soup.find("h1")
        return cleanText(nameTag.getText(separator=TAGS_TEXT_SEPARATOR))
    except:
        return DEFAULT_VALUE
    
def _getAuthorJob(soup):
    try:
        nameTag = soup.find("ul", {"class": "mr-person-job-items"})
        return cleanText(nameTag.getText(separator=TAGS_TEXT_SEPARATOR))
    except:
        return DEFAULT_VALUE
    
def _getAuthorLocation(soup):
    try:
        locationtag = soup.find("div", {"class": "person-details-item person-details-location"})
        return cleanText(locationtag.getText(separator=TAGS_TEXT_SEPARATOR))
    except:
        return DEFAULT_VALUE
    
def _getAuthorBeats(soup):
    try:
        beatsTag = soup.find("div", {"class": "person-details-item person-details-beats"})
        return cleanText(beatsTag.getText(separator=TAGS_TEXT_SEPARATOR))
    except:
        return DEFAULT_VALUE
    
def _getAuthorDescription(soup):
    try:
        descriptionTag = soup.find("div", {"class": "fs-5 fs-md-6 my-5"})
        return cleanText(descriptionTag.getText(separator=TAGS_TEXT_SEPARATOR))
    except:
        return DEFAULT_VALUE
    
def _getAsSeenIn(soup):
    try:
        seeinIn = soup.findAll('div', {'class': 'profile-details-item'})
        for span in seeinIn:
            text = cleanText(span.getText(separator=TAGS_TEXT_SEPARATOR))
            if "As seen in:" in text:
                return text.replace("As seen in:", "")
        return DEFAULT_VALUE
    except:
        return DEFAULT_VALUE    
    
def _getAuthorEmail(soup):
    try:
        contactsTag = soup.find('div', {'class':re.compile('^mr-profile-section profile-contact')})
        spans = contactsTag.findAll("span")
        for span in spans:
            text = cleanText(span.getText(separator=TAGS_TEXT_SEPARATOR))
            try:
                emailObject = validate_email(text)
                return emailObject.email
            except:
                pass
        return DEFAULT_VALUE
    except:
        return DEFAULT_VALUE
    
def _getAuthorTelephone(soup):
    try:
        contactsTag = soup.find('div', {'class':re.compile('^mr-profile-section profile-contact')})
        links = contactsTag.findAll("a")
        for link in links:
            if "tel:" in link["href"]:
                return link["href"].replace("tel:","")
        return DEFAULT_VALUE
    except:
        return DEFAULT_VALUE
    
def _getAuthorWebsiteByType(soup, type):
    try:
        contactsTag = soup.find('div', {'class':re.compile('^mr-profile-section profile-contact')})
        link = contactsTag.find("a", {"data-bs-original-title": type})
        return link["href"]
    except:
        return DEFAULT_VALUE
    
def _getTwitterFollowers(soup):
    try:
        twitterDiv = soup.find('div', {'class': 'profile-section profile-tweets mr-card'})
        links = twitterDiv.findAll('a')
        for link in links:
            strongTag = link.findAll('strong')
            if len(strongTag) == 2:
                return cleanText(strongTag[0].getText(separator=TAGS_TEXT_SEPARATOR))
        return DEFAULT_VALUE
    except:
        return DEFAULT_VALUE 

def _getTwitterTweets(soup):
    try:
        twitterDiv = soup.find('div', {'class': 'profile-section profile-tweets mr-card'})
        links = twitterDiv.findAll('a')
        for link in links:
            strongTag = link.findAll('strong')
            if len(strongTag) == 2:
                return cleanText(strongTag[1].getText(separator=TAGS_TEXT_SEPARATOR))
        return DEFAULT_VALUE
    except:
        return DEFAULT_VALUE        
    
def scrapeAuthorsLinksInfo(driver, authorLink, authorId):
    try:
        soup = navigateAndGetSoupFromDriver(driver, authorLink)

        profileTab = soup.find("div", {"class" :  re.compile("^profile-section profile-intro")}) 
        profileTab = profileTab.find("div", {"class" :  re.compile("^mr-card-content")}) 

        author = Author()
        author.id = authorId
        author.link = authorLink
        author.name = _getAuthorName(soup)
        author.job = _getAuthorJob(soup)
        author.location = _getAuthorLocation(soup)
        author.beats = _getAuthorBeats(soup)
        author.description = _getAuthorDescription(soup)
        author.seenIn = _getAsSeenIn(soup)
        author.email = _getAuthorEmail(soup)
        author.telephone = _getAuthorTelephone(soup)
        author.website = _getAuthorWebsiteByType(soup, "Blog")
        author.facebook = _getAuthorWebsiteByType(soup, "Facebook")
        author.twitter = _getAuthorWebsiteByType(soup, "Twitter")
        author.linkedin = _getAuthorWebsiteByType(soup, "LinkedIn")
        author.instagram = _getAuthorWebsiteByType(soup, "Instagram")
        author.threads = _getAuthorWebsiteByType(soup, "Threads")
        author.twitterFollower = _getTwitterFollowers(soup)
        author.twitterTweets = _getTwitterTweets(soup)

        if author.website == DEFAULT_VALUE:
            author.website = _getAuthorWebsiteByType(soup, "Website")      
        return author
    except:
        return None
