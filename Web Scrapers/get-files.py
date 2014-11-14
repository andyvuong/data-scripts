"""
" This script downloads files from a webpage to a folder in the same directory as this script.
" It works by scraping the HTML, extracting the links, and downloading files using
" appropriately parsed links.
"
" @author Andy Vuong
"
"""
# note to self: Make more "pythonic" later.

from lxml import html
from lxml import etree
import requests, urllib.request, urllib.parse, sys, re, os

######## Functions ########

"""
" @param param_url - A valid url to scrape html from.
" @param path - The path to store downloaded files.
"""
def getFiles(param_url, path):
    # Make an HTTP request to the given URL.
    response = urllib.request.urlopen(param_url)
    # Extract and print response meta-data.
    header = response.info()
    # Print the response to console.
    print("URL:",response.geturl())
    print("Status:", response.getcode())
    print(header)
    # Extract content.
    data = response.read()
    data_tree = etree.HTML(data)
    # Extract all the anchors.
    data_tree_links = data_tree.xpath('//a/@href')
    # Process all elements.
    data_processed = get_valid_files(data_tree_links)

    # Process all links.
    for n in range(0, len(data_processed)-1):
        link = data_processed[n]
        
        check = urllib.request.Request(data_processed[n])
        r = urllib.request.urlopen(check)

        link_header = r.info()
        # Check for content-type in the header
        if 'Content-Type' in link_header:
            link_filetype = link_header.get_content_subtype() #email.message.Message
            if should_download(link_filetype) == True:
                download_file(link, link_header, path)
        r.close()
                
    response.close()

"""
" @param link - Where the file is coming from.
" @param dest - Destination folder to download to.
" @param header - link's response header.
"""
def download_file(link, link_header, dest):
    name = ""
    # Analysis the header to determine the file name
    if 'Content-Disposition' in link_header:
        name = link_header.get_filename()
    else:
        name = basename(urlsplit(link)[2])
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), dest)
    final_dest = os.path.join("/test/", name)
    print(final_dest)
    # Download
    urllib.request.urlretrieve(link, final_dest)
    

"""
" @param content_type - content type of file
" @return true if the file should be downloaded
"""
def should_download(content_type):
    acceptable = ['pdf'] # list of acceptable content types
    for n in acceptable:
        if n == content_type:
            return True
    return False

"""
" @param array_data - An array of string elements.
" @return array_valid_data - A string array of valid urls.
"""
def get_valid_files(array_data):
    array_valid_data = []
    # Process array.
    for n in range(0, len(array_data)-1):
        link = is_valid_url(array_data[n])
        # Link is valid.
        if link is not None:
            array_valid_data.append(link.group(0))
    # Return array of valid links to try.
    return array_valid_data
        
"""
" External Resource, I do not claim ownership of the below function.
" URL validator used by django
" Source: https://github.com/django/django/blob/master/django/core/validators.py
"
" @param url - a string.
" @return 'match object' or None
"""
def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


######## Run Script ########
        
#getFiles("https://wiki.cites.illinois.edu/wiki/display/cs233fa14/Assignments", "test")
getFiles("https://courses.engr.illinois.edu/cs225/resources.htm", "test")


