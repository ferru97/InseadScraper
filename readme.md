# Install
## Create virtual enviroment (only first ime)
`py -m venv venv to create the virtual environment`

## Activate virtual environment
`.\venv\Scripts\activate`

## Install dependencies
`pip install -r requirements.txt`

# Run script

## Download list of authors
`py mail.py --file journals.csv --action authorList`

## Download general information for each author
`py main.py --file users.csv --action authorInfo`

## Download articles for each author
`py main.py --file users.csv --action authorArticles --max-articles 25`

## Download tweets for each author
`py main.py --file users.csv --action authorTweets --max-tweets 30`