import pymongo
import elasticsearch
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from lxml import html
import requests


######## Functions ########
def getFiles(param_url):
    print(">Running getFiles script.")
    
    url = param_url
    print(">Accessing: " + url)
    
    page = requests.get(url)
    tree = html.fromstring(page.content)
    filename = tree.xpath('//a/@href')

    print(">Printing results of extract:")
    for n in range(0, len(filename)-1):
        print("+1")
        print(filename[n])

    print(">This script is incomplete. Script ending.")

######## Run Script ########
        
getFiles("https://subversion.ews.illinois.edu/svn/fa14-cs241/_shared/past-lectures/")
