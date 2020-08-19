#imports
from bs4 import BeautifulSoup
import requests
import pandas as pd


#global variables
label_lists = [[] for i in range(4)]
datatype_list = ["APIS", "TM", "DCLP", "HGV"]

def main():
    """
    Designed to scrape the specific labels from the Papyri.info website
    """
    webpage = requests.get("http://papyri.info/search?STRING=%28magical%29&no_caps=on&no_marks=on&target=metadata&DATE_MODE=LOOSE&DOCS_PER_PAGE=1000")
    papyri_search = webpage.content
    soup = BeautifulSoup(papyri_search, "html.parser")
    raw_links = soup.find_all('a')
    links = ["http://papyri.info"+link.get('href') for link in raw_links]
    del links[:11] #links as raw has a lot of garbage extra links not in the search table
    del links[-14:] #these two lines remove the unneeded ones. Improvements to come
    for link in links:
        webpage = requests.get(link)
        papyrus = webpage.content
        papyrus_soup = BeautifulSoup(papyrus, "html.parser")
        try:
            controls = papyrus_soup.findAll("label")
            for tag in controls:
                #print(tag.text)
                label_search = datatype(tag.text)
                if label_search is not None:
                    table = papyrus_soup.find("div", attrs={"class": label_search})
                    for th in table.findAll('th'):
                        table_append(label_search, th.string.strip())
        except AttributeError:
            continue
    label_lists2 = [list(dict.fromkeys(i)) for i in label_lists]
    labeldf = pd.DataFrame(label_lists2)
    labeldf.to_csv(r"C:\Users\Alex\Documents\Coding\label_lists.csv")




def datatype(tag):
    """
    Quickly returns the best value to input into Beautiful Soup to determine the table type
    """
    for i in datatype_list:
        if i in tag:
            return i.lower()+" data"
        return None

def table_append(label_search, th):
    """
    Adds the value to the appropriate table
    """
    j = 0
    for i in datatype_list:
        if i.lower() in label_search:
            label_lists[j].append(th)
        j += 1

    
if __name__ == "__main__":
    main()