## About
This software is written for a graduation project at the University of Twente. The goal of the project 
is to evaluate posts on the Kindertelefoon forum and to assess which posts require an empathetic response.
This can be used to alert an adult volunteer to respond to a certain topic. This evaluation is achieved by first classifying empathetic responses, and through determining to which post the empathic post is responding, classifying posts which call for empathy. 

For this, a BERT model and an LSTM model were used. The main goal of these models is to determine which posts express empathy, but in an exploratory study they are also trained on the call for empathy detection directly.

## Scraper
To gain the data to be used in the project, the forum from the Kindertelefoon was scraped. The scraper
can be used with a comma separated file of urls, a single URL or a downloaded HTML file. 

If a file of urls is used, it should be passed as an argument as follows:

`soupcrawler.py crawlfile=path/to/crawlfile.csv`

If a url is used, it should be passed as an argument as follows:

`soupcrawler.py url=https://www.kindertelefoon.nl/topic/thread/`

If an HTML file is used it should be passed as an argument as follows:

`soupcrawler.py html=path/to/htmlfile.html`

The scraper will scrape usernames, userIDs, posts, dates, likes, usermentions and user titles from 
the posts on the forum as well as the tags and topic of the thread.

## Dependency builder
The dependency builder automatically labels relations between posts based on similarity, temporal 
proximity and content type.

## Flasksite
The website maintained in the Flasksite directory hosts a page on which annotators can annotate the scraped data. This is necessary for the supervised training of the models. 

## Language model
The language model directory holds the BERT and LSMT models. The BERTje pretrained model is used with additional pretraining steps on the Kindertelefoon data.












