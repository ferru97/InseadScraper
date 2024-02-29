import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from src.utils.SeleniumUtils import getSoupFromDriver, navigateAndGetSoupFromDriver
from urllib.parse import urlsplit, urlunsplit
from src.model.Article import Article
from src.utils.Utils import cleanText
import pandas as pd

DEFAULT_VALUE = "--"
TAGS_TEXT_SEPARATOR = " "

def loadAllArticles(driver, maxArticles):
    try:
        lastArticleSize = 0
        while True:
            soup = getSoupFromDriver(driver)
            articles = soup.findAll("div", {"class": "news-story"})
            if lastArticleSize == len(articles) or len(articles)>=maxArticles:
                try:
                    moreButton = driver.find_element(By.XPATH,"//a[text()='Show More']")
                    moreButton.click()
                    time.sleep(4)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                except:
                    return articles
            else:
                lastArticleSize = len(articles)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(4)
    except:
        return list()
    

def _getArticleTitle(soup):
    try:
        titleTag = soup.find("h4")
        return cleanText(titleTag.getText(separator=TAGS_TEXT_SEPARATOR))
    except:
        return DEFAULT_VALUE
    
def _getArticleLink(soup):
    try:
        titleTag = soup.find("h4")
        linkTag = titleTag.find("a")
        return linkTag["href"]
    except:
        return DEFAULT_VALUE
    
def _getArticleDate(soup):
    try:
        dateTag = soup.find("a", {"class": "text-muted timeago"})
        return dateTag["datetime"]
    except:
        return DEFAULT_VALUE    
    
def _getArticleAuthors(soup):
    try:
        articleTag = soup.find('div', {'class':re.compile('^news-story-body')})
        authorsTag = articleTag.findAll("a")
        authors = [cleanText(a.getText(separator=TAGS_TEXT_SEPARATOR)) for a in authorsTag]
        return ",".join(authors[1:])
    except:
        return DEFAULT_VALUE
    
def _getArticleDescription(soup):
    try:
        articleTag = soup.find('div', {'class':re.compile('^news-story-body')})
        articleTag.find('div').decompose()
        return cleanText(articleTag.getText(separator=TAGS_TEXT_SEPARATOR))
    except:
        return DEFAULT_VALUE
    
def scrapeAuthorArticles(driver, authorLink, authorId, maxArticles):
    try:
        soup = navigateAndGetSoupFromDriver(driver, authorLink + "/articles")
        articlesTab = loadAllArticles(driver, maxArticles)

        articles = list()
        for articleTab in articlesTab:
            newArticle = Article()
            newArticle.authorId = authorId
            newArticle.title = _getArticleTitle(articleTab)
            newArticle.link = _getArticleLink(articleTab)
            newArticle.date = _getArticleDate(articleTab)
            newArticle.authors = _getArticleAuthors(articleTab)
            newArticle.description = _getArticleDescription(articleTab)
            articles.append(newArticle)
        return articles
    except:
        return list()
