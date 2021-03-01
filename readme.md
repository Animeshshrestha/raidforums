**RaidForum Scraping**

[RaidForum](http://raidforums.com/)- Official Link to the website

<u>Technologies Used</u>  
- Backend: Python, Scrapy, Postgresql, SQLAlchemy

# Project Installation:
1. Setup the virtual environment
2. Clone the github repository into your terminal
3. Run the command
```bash
pip install -r requirements.txt
```
4. Please change the credientals for postgres connection which is located on raidforums/settings.py
```
CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}".format(
    drivername="postgresql",
    user="postgres", # change this
    passwd="admin", #change this
    host="localhost",
    port="5432",
    db_name="raidforums_db", #put here db name according to the db you have created on postgres
)
```
5. Use the below command to run the spider
```
scrapy crawl raidforum_spider
```

# Task Completed
1. Scraping the content of all the section
2. Saving the scraped content to the database

# Task Not completed
1. Scraping after user is logged in
2. Have not completed the further scraping of the posts inside forum
3. Rotating Proxies and User Agent dynamic changes not setup.

# Known Issue
1. If we try to scrape the data multiple times then we will be blocked by raidforums.

