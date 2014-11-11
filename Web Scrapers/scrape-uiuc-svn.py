from lxml import html
from lxml import etree
import requests
import urllib.request
import sys
import re
import os

######## Functions ########
def getFiles(param_url, path):
  
    response = urllib.request.urlopen(param_url)
  
    # Extract and print response meta-data
    header = response.info()
    
    # Print the response to console
    print("URL:",response.geturl())
    print("Status:", response.getcode())
    print(header)

    # Extract content
    data = response.read()
    data_tree = etree.HTML(data)
    
    # Extract all the anchors
    data_tree_links = data_tree.xpath('//a/@href')
    #print(data_tree_links)

    # Download files
    #dest_directory = os.path.join(os.path.dirname(os.path.abspath(_file_)), "test")
    #urllib.request.urlretrieve("http://www.andyvuong.me/resources/avresume.pdf", os.path.join("test", "file.pdf"))

    
    for n in range(0, len(data_tree_links)-1):
        print(data_tree_links[n])
        

    response.close()

    
######## Run Script ########
        
getFiles("https://wiki.cites.illinois.edu/wiki/display/cs233fa14/Assignments", "test")
#getFiles("http://en.wikipedia.org/wiki/Wormhole")
