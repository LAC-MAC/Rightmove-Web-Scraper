import requests
from bs4 import BeautifulSoup
import json
import re
import math


#Object for a property featured on Rightmove

class Property:
  def __init__(self, id, address, price, numOfBeds, summary, agent):
    self.id = id
    self.address = address
    self.price = price
    self.numOfBeds = numOfBeds
    self.summary = summary
    self.agent = agent


#This method parses the response from html soup to find the properties which are json objects
# and adds them to a list.

def parseJson(soup, propertyList):
    results = soup.find_all('script')

    for i in results:
        if "window.jsonModel = {\"properties\":" in i.getText():
            
            properties = re.search('(?<=window\.jsonModel = ).*', i.getText())
            rawJson = properties.group(0)

    jObj = json.loads(rawJson)

    indivProps =jObj["properties"]

    for i in indivProps:
        prop = Property(i['id'], i['displayAddress'], i['price']['amount'], i['bedrooms'], i['summary'], i["customer"]["branchDisplayName"])
        propertyList.append(prop)

#This method calculates how many pages the search returns

def calcPage(soup):
    numberOfProp = soup.findAll('span', class_="searchHeader-resultCount")
    total = int(numberOfProp[0].getText())

    numberOfPages = math.ceil(total / 25)

    return numberOfPages


#Print all properties that match the given critera
def printMatches(numOfBeds, price):
    index = 0

    for i in propertyList:
    
        if i.numOfBeds >= numOfBeds and i.price < price:
            index = index+1
            print("---------------------------")
            print(i.id)
            print(i.address)
            print(i.numOfBeds)
            print(i.price, "\n")

            print(i.summary, "\n")
            print(i.agent, "\n")
        

    print("Total Number Of Results: ", index)


## First Base URL and User Agent

baseURL = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93616&radius=3.0&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'
}


#Request

r = requests.get(baseURL)

#empty property list
propertyList = []


soup = BeautifulSoup(r.content, 'lxml')

#Calculate number of pages
numberOfPages = calcPage(soup)


#parse response
parseJson(soup, propertyList)
    
   

#loop for how many pages there are
for i in range(numberOfPages):
    #calculate the new index number for each additional page
    index = (i+1)*24
    
    #Create new URL
    baseURL = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E93616&radius=3.0&index={p}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords='.format(p =index)

    #Request
    r = requests.get(baseURL)

    soup = BeautifulSoup(r.content, 'lxml')

    #parse
    parseJson(soup, propertyList)




#Print matches based on critera of 4 bedroom under the price of £2000
printMatches(4, 2000)





        
    
        
        












