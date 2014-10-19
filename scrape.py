import pymongo
import elasticsearch
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from lxml import html
import requests


#s_ string type
#p_ parameter type

es = Elasticsearch()

# Makes an api call with an indeed publisher's id
def queryJobs(q, l, jt, co, limit, radius, latlong):
    publisher = 6603890256880438
    # important publisher info (private)
    # Set params.
    p_q = q
    p_l = l
    p_jt = jt
    p_co = co
    p_limit = limit
    p_radius = radius
    p_latlong = latlong
    url = "http://api.indeed.com/ads/apisearch?"

    # Assemble the url.
    getUrl = url + "publisher=" +str(publisher) + "&q=" + p_q + "&l=" + p_l + "&jt=" + p_jt + "&co=" + p_co + "&limit=" + p_limit + "&radius=" + p_radius + "&latlong=" + p_latlong + "&v=2"

    print(getUrl)
    page = requests.get(getUrl)
    tree = html.fromstring(page.content)
    
    # Scrape the elements.
    
    s_jobtitle = tree.xpath('//jobtitle/text()')
    s_company = tree.xpath('//company/text()')
    s_city = tree.xpath('//city/text()')
    s_state = tree.xpath('//state/text()')
    s_date = tree.xpath('//date/text()')
    s_snippet = tree.xpath('//snippet/text()')
    s_url = tree.xpath('//url/text()')
    s_long = tree.xpath('//longitude/text()')
    s_lat = tree.xpath('//latitude/text()')
    s_formattedRelativeTime = tree.xpath('//formattedRelativeTime/text()')
    
    #print(len(s_jobtitle))
    lengthArray = [ len(s_jobtitle), len(s_company), len(s_city), len(s_state),
                    len(s_date), len(s_snippet), len(s_url), len(s_long), len(s_lat)]
    minLen = min(lengthArray)
    #print(minLen)

    for n in range(0, minLen-1): 
        doc = {
            'jobtitle':s_jobtitle[n],
            'company': s_company[n],
            'city': s_city[n],
            'state': s_state[n],
            'date': s_date[n],
            'snippet': s_snippet[n],
            'longitude': s_long[n],
            'latitude': s_lat[n],
            'url': s_url[n],
          #  'formattedRelativeTime': s_formattedRelativeTime[n]            
        }
        res = es.index(index="jobs", doc_type="posts", id=n, body=doc)
        #print("running: " + str(n))


qArray = [ "software", "internship", "university",
           "software internship", "software engineer",
           "software engineering intern", "software developer", "Information Technology",
           "marketing", "finance", "Industrial", "medical", "professor", "technician"]

locationArray = ["chicago", "San Francisco", "Texas", "New York", "Seattle", "Los Angeles",
                    "Detroit", "Pheonix", "Washington D.C.", "Denver", "Boston", "Philidelphia",
                 "Miami", "Indianapolis", "St. Louis", "Atlanta", "San Jose", "Mountain View",
                 "Redwood City", "Cupertino", "San Diego", "Providence", "Albany", "New Mexico City",
                 "Austin", "Pittsburg"]

for strings in qArray:           
    for city in locationArray:
        queryJobs(strings, city, "", "usa", "20", "25", "1")

es.indices.refresh(index="jobs")
