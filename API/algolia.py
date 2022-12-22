# hello_algolia.py
from os import getenv

from algoliasearch.search_client import SearchClient
from algoliasearch.search_index import SearchIndex
from dotenv import load_dotenv, find_dotenv
from fastapi import HTTPException, status
import pandas as pd

load_dotenv(find_dotenv())

APP_ID = getenv('APP_ID')
API_SEARCH_KEY = getenv('API_SEARCH_KEY')
DB_NAME = getenv('DB_NAME')

def initialize_database():
    # Connect and authenticate with your Algolia app
    try:
        global client 
        client = SearchClient.create(APP_ID, API_SEARCH_KEY)
        global KPMG_index 
        KPMG_index = client.init_index(DB_NAME)

        print("Initialized Algolia connection")
    except:
        raise Exception("unable to connect to Algolia search client")

def get_CLAs():
    CLAs = KPMG_index.search('')

    return CLAs["hits"]

def get_CLA_by_id(id):
    try:
        CLA = KPMG_index.get_object(id)
    except:
       raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="CLA for given id doesn't exist"
        )

    return CLA

def get_CLA_by_name(name):
    try:
        CLA = KPMG_index.search(name)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="CLA for given name doesn't exist"
        )

    return CLA

def get_CLAs_by_keyword(keyword):
    try:
        CLAs = KPMG_index.search(keyword, {

        })
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="CLA for given name doesn't exist"
        )

    return CLAs["hits"]

def get_Comparison(id):
    try:
        CLA = get_CLA_by_id(id)
        if CLA["parent"]!="":
            comparison = CLA["summaryCompareParent"]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="no parent for this CLA"
        )

    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="CLA for given id doesn't exist"
        )

    return comparison

# initialize_database()

# res = get_Comparison("200-2020-000391")

# print(res)
# initialize_database()
# print(get_CLAs())