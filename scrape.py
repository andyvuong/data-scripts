import pymongo
from pymongo import MongoClient
from lxml import html
import requests


#s_ string type
#p_ parameter type

client = MongoClient()
db = client.boilermake


# Makes an api call with an indeed publisher's id
def queryJobs(q, l, jt, co, limit, radius, latlong):
    publisher = xxxxxxxxxxxxx # important publisher info (private)
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
    #print(len(s_jobtitle))

    for n in range(0, len(s_jobtitle)): 
        db.jobs.insert(
            {
             "jobtitle": s_jobtitle[n],
             "company": s_company[n]
            }
        )
    posts = db.posts
    posts.find_one()


queryJobs("internships", "chicago", "usa", "internship", "20", "10", "1")

