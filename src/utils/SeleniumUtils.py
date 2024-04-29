import os
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc 
from selenium import webdriver
from bs4 import BeautifulSoup

CHROME_DRIVER_PATH = "resources/chromedriver.exe"
FIREFOX_DRIVER_PATH = "resources/geckodriver.exe"


def getSeleniumInstanceFirefox():
    chrome_options = Options()
    #chrome_options.add_argument("user-agent="+user_agent)
    chrome_options.add_argument("--user-data-dir=C:/Users/Vito/AppData/Local/Google/Chrome/User Data")
    chrome_options.add_argument('--profile-directory=Default')
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def getTestDriver(chromeVersion):
    options = uc.ChromeOptions() 
    options.headless = False
    driver = uc.Chrome(use_subprocess=True, options=options, version_main=chromeVersion) 
    return driver


def navigateAndGetSoupFromDriver(driver, link):
    driver.get(link)
    time.sleep(3)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    return BeautifulSoup(html, 'html.parser')

def getSoupFromDriver(driver):
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    return BeautifulSoup(html, 'html.parser')