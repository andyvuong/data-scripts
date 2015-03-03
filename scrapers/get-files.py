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
    num_processed = 0
    num_downloads = 0
    num_failures = 0
    
    try:
        print("Making a request to server...")
        urllib.request.urlopen(param_url)
    except urlliab.error.HTTPError as e:
        print("Error: " + str(e.code))
        print(e.read())
    else:
        print("Success! Returning the header information: \n")
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
        print("Extracted valid urls")
        
        # Process all links.
        print("Processing...")

        for link in data_processed:
            check = urllib.request.Request(link)
            try:
                urllib.request.urlopen(check)
            except urllib.error.HTTPError as e:
                print("Error: " + str(e.code))
                print(e.read())
                print("Continuing...")
                num_failures += 1
            else:   
                r = urllib.request.urlopen(check)
                link_header = r.info()
                # Check for content-type in the header
                if 'Content-Type' in link_header:
                    link_filetype = link_header.get_content_subtype() #email.message.Message
                    if should_download(link_filetype) is True:
                        download_file(link, link_header, path)
                        num_downloads += 1
                r.close()
            num_processed += 1

        # Return:
        print("\n\n####PROCESS FINISHED####")
        print("Processed valid links: " + str(num_processed))
        print("Number of downloads: " + str(num_downloads))
        print("Number of failures: " + str(num_failures))

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
    if os.path.exists(directory) is False:
        os.mkdir(directory, 0o777)
    
    # Create the specified path if necessary
    final_dest = os.path.join(directory, name)
    print("Downloaded File: " + name)
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
    for link in array_data:
        valid_link = is_valid_url(link)
        # Link is valid.
        if valid_link is not None:
            array_valid_data.append(valid_link.group(0))
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
        
getFiles("https://courses.engr.illinois.edu/cs225/resources.htm", "documents")


