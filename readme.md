# Install
## Create virtual enviroment (only first ime)
`py -m venv venv`

## Activate virtual environment
`.\venv\Scripts\activate`

## Install dependencies
`pip install -r requirements.txt`

# Run script

## Download list of authors
`py mail.py --file journals.csv --action authorList  --chrome-version 123`

## Download general information for each author
`py main.py --file users.csv --action authorInfo  --chrome-version 123`

## Download articles for each author
`py main.py --file users.csv --action authorArticles --max-articles 25  --chrome-version 123`

## Download tweets for each author
`py main.py --file users.csv --action authorTweets --max-tweets 30  --chrome-version 123`
