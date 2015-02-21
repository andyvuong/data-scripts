import shutil
from bs4 import BeautifulSoup
import os
from os.path import basename


# Filter out the posts that are 
# are not found. They should be the
# html piages with "standard_error"
def filter_posts(filepath):
    for file in os.listdir(filepath):
        file_dat = open("data_1/" + str(file), 'r').read()
        soup = BeautifulSoup(file_dat)
       
        a = soup.find_all("div", class_="standard_error")
        if(len(a) > 0):
            os.remove("data_1/" + str(file))

def deeper_filter(filepath):
    url_l = "http://estetica-design-forum.com/showthread.php?"
    for file in os.listdir(filepath):
        s = file.find('_')        
        e = file.find('.')
        k = file[s+1:e]
        url_f = url_l + k
        #print(url_f)
        f = open('avuong3_txt/avuong3_' + k + ".txt", 'wb')
        f.write(url_f + '\n')

        file_dat = open("data_1/" + str(file), 'r').read()
        soup = BeautifulSoup(file_dat)
        title = soup.find('title')
        if title is not None:
            w_title = title.getText().encode('utf-8').strip()
            f.write(w_title + '\n')
        
        #print(w_title)

        posts = soup.find_all("div", class_="content")
        if posts is not None:
            for items in posts:
                w_content = items.text.encode('utf-8').replace('\n',' ').strip()
                #print(w_content)
                f.write(w_content + '\n')
        f.close()

filter_posts("data_1")
deeper_filter("data_1")


            
