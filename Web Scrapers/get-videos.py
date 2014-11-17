import urllib.request, sys, re, os
import json, codecs



def get_videos(path):
    response = urllib.request.urlopen(path)
    header = response.info()
    print("URL: ", response.geturl())
    print("Status: ", response.getcode())
    print(header)
    
 #   data = json.load(urllib.request.urlopen("http://recordings.engineering.illinois.edu/ess/portal/section/b8ba65b2-9808-432f-aec8-877be1c907f2/section-data.json?pageSize=100"))

 #   directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")


 #   if os.path.exists(directory) is False:
 #       os.mkdir(directory, 0o777)

 #   final_dest = os.path.join(directory, "vid.html")
 #   urllib.request.urlretrieve(path, final_dest)
 #   response.close()




#get_videos("http://recordings.engineering.illinois.edu/ess/echo/presentation/a1323faa-e6e4-4f31-b1fc-8c0308b2617c?ec=true")
