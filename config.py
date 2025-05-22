"""Establish hyperparameters to be used with all the scripts, 
avoiding redundant hardcoding."""

BASE_URL = "http://export.arxiv.org/api/query?"

# search parameters
SEARCH_QUERY = "all:nanoparticles+AND+all:triple+negative+breast+cancer"

RAW_CSV_PATH = "data/nano_tnbc_arxiv.csv"