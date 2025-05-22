"""Testing the scraper on a small dataset to see if results are getting
scraped correctly."""

import pandas as pd
import urllib.request
import feedparser
import time

BASE_URL = "http://export.arxiv.org/api/query?"

# search parameters
SEARCH_QUERY = "all:nanoparticles+AND+all:triple+negative+breast+cancer"

RAW_CSV_PATH = "data/nano_tnbc_arxiv.csv"

START = 0
TOTAL_RESULTS = 5
RESULTS_PER_ITERATION = 5
WAIT_TIME = 3 

def fetch_records():
    """Page through results until TOTAL_RESULTS are collected."""
    # create a dictionary with necessary information
    results_dict = {
        "arXiv_id":[],
        "Title":[],
        "Date_Published":[],
        "Abstract":[]
    }
    
    for i in range(START, TOTAL_RESULTS, RESULTS_PER_ITERATION):
        print("Results %i - %i" % (i, i+RESULTS_PER_ITERATION))
        QUERY = "search_query=%s&start=%i&max_results=%i" % (SEARCH_QUERY, 
                                                            i, 
                                                            RESULTS_PER_ITERATION)
        
        # perform GET request with base_url and query
        response = urllib.request.urlopen(url=BASE_URL+QUERY, data=None)
        
        feed = feedparser.parse(response)
        
        # print out feed information
        print("Feed title: %s" % feed.feed.title)
        print("Feed last updated: %s" % feed.feed.updated)

        # print opensearch metadata
        print("totalResults for this query: %s" % feed.feed.opensearch_totalresults)
        print("itemsPerPage for this query: %s" % feed.feed.opensearch_itemsperpage)
        print("startIndex for this query: %s" % feed.feed.opensearch_startindex)
        
        # run through each entry, and extract necessary information
        for entry in feed.entries:
            arxivID = entry.id.split("/abs/")[-1]
            year = entry.published[:4] # only grab the year
            title = entry.title
            abstract = entry.summary
            
            results_dict["arXiv_id"].append(arxivID)
            results_dict["Date_Published"].append(year)
            results_dict["Title"].append(title)
            results_dict["Abstract"].append(abstract)
        
        # sleep before calling API again
        time.sleep(WAIT_TIME)
    
    print("Total collected:", len(results_dict["arXiv_id"]))
    return results_dict
        
def save_raw(results_dict):
    import os
    os.makedirs("data", exist_ok=True)
    
    df = pd.DataFrame(results_dict)
    df.to_csv(RAW_CSV_PATH, index=False)

if __name__=="__main__":    
    rec = fetch_records()
    save_raw(rec)