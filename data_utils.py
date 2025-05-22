"""Send requests for search queries, save data to DataFrame and CSV file.
Uses arXiv API for querying research papers."""

import requests 
import pandas as pd
import urllib.request
import feedparser
import time

from config import BASE_URL, SEARCH_QUERY, RAW_CSV_PATH


START = 0
TOTAL_RESULTS = 1000
RESULTS_PER_ITERATION = 200
WAIT_TIME = 3 

def fetch_records():
    """Page through results until TOTAL_RESULTS are collected."""
    # create a dictionary with necessary information
    results_dict = {
        "arXiv_id":[],
        "Title":[],
        "year":[],
        "Abstract":[]
    }
    
    for i in range(START, TOTAL_RESULTS, RESULTS_PER_ITERATION):
        QUERY = "search_query=%s&start=%i&max_results=%i" % (SEARCH_QUERY, 
                                                            i, 
                                                            RESULTS_PER_ITERATION)
        
        # perform GET request with base_url and query
        response = urllib.request.urlopen(url=BASE_URL+QUERY, data=None)
        
        feed = feedparser.parse(response)
        
        # run through each entry, and extract necessary information
        for entry in feed.entries:
            arxivID = entry.id.split("/abs/")[-1]
            year = entry.published[:4] # only grab the year
            title = entry.title
            abstract = entry.summary
            
            results_dict["arXiv_id"].append(arxivID)
            results_dict["year"].append(year)
            results_dict["Title"].append(title)
            results_dict["Abstract"].append(abstract)
        
        # sleep before calling API again
        time.sleep(WAIT_TIME)
    
    return results_dict
        
def save_raw(results_dict):
    import os
    os.makedirs("data", exist_ok=True)
    
    df = pd.DataFrame(results_dict)
    df.to_csv(RAW_CSV_PATH, index=False)