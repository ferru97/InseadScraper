import os
import sys
import time
import logging
import argparse
#import validators
import pandas as pd
from urllib.parse import urlparse
from src.utils.SeleniumUtils import getSeleniumInstanceFirefox, getTestDriver
from src.model.Journal import Journal
from src.engine.AuthorScraperEngine import scrapeAuthorsLinks
from src.engine.AuthorInfoScraperEngine import scrapeAuthorsLinksInfo
from src.engine.AuthorArticlescraperEngine import scrapeAuthorArticles
from src.engine.AuthorTweetScraperEngine import scrapeAuthorsTweets

INPUT_FILE_DIRECTORY = "input/"
OUTPUT_FILE_DIRECTORY = "output/"

ACTIONS_LIST = ["authorList", "authorInfo", "authorArticles", "authorTweets"]

DF_PROCESSED = "processed"

def _saveData(outputFileName, dataList):
    data = [d.getCsvRecord() for d in dataList]
    outputFilePath = os.path.join(OUTPUT_FILE_DIRECTORY, outputFileName)
    withHeaderRestaurant = os.path.exists(outputFilePath) == False
    outputDf = pd.DataFrame(data)
    outputDf.to_csv(outputFilePath, sep=';', quotechar='"', encoding='utf-8', mode='a', header=withHeaderRestaurant, index=False)

def _updateInputFile(filename, df):
    inputFilePath = os.path.join(INPUT_FILE_DIRECTORY, filename)
    df.to_csv(inputFilePath, index=False)     


def _loadJournals(filename):
    inputFilePath = os.path.join(INPUT_FILE_DIRECTORY, filename)
    df = pd.read_csv(inputFilePath)
    if not DF_PROCESSED in df.columns:
        df[DF_PROCESSED] = "N"
        df.to_csv(inputFilePath, index=False)    
    
    journalsList = list()
    for _, journal in df.iterrows():
        newJournal = Journal()
        newJournal.id = journal["id"]
        newJournal.name = journal["name"]
        newJournal.processed = journal["processed"]
        newJournal.link = journal["link"]
        journalsList.append(newJournal)

    logging.info(f'Loaded dataset with {len(df.index)} journals')
    return journalsList

def _loadAuthors(filename, processedHeader):
    inputFilePath = os.path.join(INPUT_FILE_DIRECTORY, filename)
    df = pd.read_csv(inputFilePath)
    if not processedHeader in df.columns:
        df[processedHeader] = "N"
        df.to_csv(inputFilePath, index=False)    

    logging.info(f'Loaded dataset with {len(df.index)} authors')
    return df

def _login(driver):
    driver.get("https://insead.muckrack.com/")
    input("Login, accept cookie and and press ENTER to continue")

def _runAuthorsList(journalsFileName, driver):
    logging.info(f"Start authors link'\n") 
    journals = _loadJournals(journalsFileName)
    for journal in journals:
        logging.info(f"Start scraping authors for journal '{journal.name}'\n")
        scrapeAuthorsLinks(driver, journal.link, OUTPUT_FILE_DIRECTORY)


def _main(authorsFileName, driver, action, processedHeader, outputFileName, maxArticles, maxTweets):
    logging.info(f"Start authors information'\n") 
    authors = _loadAuthors(authorsFileName, processedHeader)
    totalAuthors = len(authors.index)
    data = list()
    for index, row in authors.iterrows():
        authorLink = row["LINK"]
        logging.info(f"{index+1}/{totalAuthors} Start scraping for authors '{authorLink}'\n")
        if (row[processedHeader] == "Y"):
            logging.info(f"Skip author '{authorLink}' already processed...\n")
            continue

        elif action == "authorInfo":
            data = scrapeAuthorsLinksInfo(driver, authorLink, row["ID"])
            data = [data]
        elif action == "authorArticles":
            data = scrapeAuthorArticles(driver, authorLink, row["ID"], maxArticles)
        elif action == "authorTweets":
            data = scrapeAuthorsTweets(driver, authorLink, row["ID"], maxTweets)    

        data = [d for d in data if d != None]
        if len(data) > 0:
            authors.loc[index, processedHeader] = "Y"
            _saveData(outputFileName, data)
            _updateInputFile(authorsFileName, authors)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
    logging.info("Insead Scraper!\n")

    parser = argparse.ArgumentParser(description='Insead Scraper')
    parser.add_argument('--file', required=True, help='input journals file name')
    parser.add_argument('--max-articles', required=True, default=0, help='Maximum number of article to fetch for each author')
    parser.add_argument('--max-tweets', required=True, default=0, help='Maximum number of tweer to fetch for each author')
    parser.add_argument('--action', required=True, help='authorList: Download author list - authorInfo: Download author info - authorArticles: Download author articles - authorTweet: download author tweer')
    args = parser.parse_args()

    driver = getTestDriver()
    _login(driver)

    if args.action == "authorList":
        _runAuthorsList(args.file, driver)
    elif args.action in ACTIONS_LIST:
        _main(args.file, driver, args.action, args.action + "_PROCESSED", args.action + ".csv", int(args.max_articles), int(args.max_tweets)) 
    else:
        logging.info("Invalid action, it must  be one of the following {ACTIONS_LIST}\n")

    driver.close()
    print("Done :)")


# aileen.huang@insead.edu
#p/w: inseadaileen        