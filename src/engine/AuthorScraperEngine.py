import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from src.utils.SeleniumUtils import getSoupFromDriver, navigateAndGetSoupFromDriver
from urllib.parse import urlsplit, urlunsplit
import pandas as pd

def loadAllAuthors(soup, driver):
    authorTabs = list()
    try:
        lastAuthorSize = 0
        while True:
            soup = getSoupFromDriver(driver)
            contantTab = soup.find("div", {"id": "mr-results-content-person"})
            authorTabs = contantTab.findAll("div", {"id" :  re.compile("^result-person-")})     
            if lastAuthorSize == len(authorTabs):
                try:
                    moreButton = driver.find_element(By.XPATH,"//a[text()='Show More']")
                    moreButton.click()
                    time.sleep(4)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                except:
                    return authorTabs
            else:
                lastAuthorSize = len(authorTabs)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(4)
    except:
        return authorTabs
    
def getUsersLink(driver, usersTabs):
    baseUrl = driver.current_url.split(".com")[0] + ".com"
    userLinks = list()
    for userTab in usersTabs:
        try:
            userLinkTag =  userTab.find("a", {"class": "js-person-name"})
            userLinks.append(baseUrl + userLinkTag["href"])
        except:
            pass    
    return userLinks

def createBaseUserDataframe(userLinks, outputDir):
    df = pd.DataFrame({"LINK": userLinks})
    df["ID"] = df.index + 1
    df["authorInfo_PROCESSED"] = "N"
    df["uthorArticles_PROCESSED"] = "N"
    df["authorTweets_PROCESSED"] = "N"
    df = df[ ['ID'] + [ col for col in df.columns if col != 'ID' ] ]
    df.to_csv(outputDir + "users.csv", index=False)
        

def scrapeAuthorsLinks(driver, journalLink, outputDir):
    soup = navigateAndGetSoupFromDriver(driver, journalLink)
    usersTabs = loadAllAuthors(soup, driver)
    usersLink = getUsersLink(driver, usersTabs)
    createBaseUserDataframe(usersLink, outputDir)
