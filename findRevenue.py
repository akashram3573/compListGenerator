import collections

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


class getCompRevenue:
    def __init__(self, compList):
        self.countOfLinks = 0
        self.countOfMacroTables = 0
        self.compRevDict = collections.defaultdict(float)
        self.compData = compList
    def getRevenue(self, mTrendLink):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        # mTrendLink = "https://www.macrotrends.net/stocks/charts/AAPL/apple/revenue"
        # mTrendLink = "https://www.macrotrends.net/stocks/charts/AAPL/apple/financial-statements"
        data = requests.get(mTrendLink, headers=headers, verify=False).text
        soup = BeautifulSoup(data, 'html.parser')

        try:
            tbList = soup.findAll('table')
            # print(tbList)
            for tb in tbList:
                if "Annual Revenue" in str(tb):
                    # print(tb)
                    revRow = tb.find('tbody').find('tr').findAll('td')
                    for row in revRow:
                        rev = row.text
                        if '$' in rev:
                            try:
                                rev = float(rev.replace("$", '').replace(',', ''))
                                self.countOfMacroTables += 1
                                # print(rev)
                                return rev / 1000
                            except:
                                rev = -1.0
                                return rev
            return -1.0
        except:
            return -1.0

    def getMacroLink(self, cName):
        data = requests.get("https://www.google.com/search?q=" + cName + "+annual+revenue+2022+macrotrends",
                            verify=False)
        data = data.text
        soup = BeautifulSoup(data, "html.parser")
        aTags = soup.findAll('a')
        # print(aTags)
        for aTag in aTags:
            # print(link)
            # print(type(link))
            link = aTag.attrs['href']
            if "https://www.macrotrends.net" in link:
                link = link[link.index("https"):]
                if "revenue" not in link:
                    continue
                self.countOfLinks += 1
                rev = self.getRevenue(link)
                self.compRevDict[cName] = rev
                # getRevenue(link[link.index("https"):])
                return
        self.compRevDict[cName] = -1.0
        return
        # for data in soup(['style', 'script']):
        #     # Remove tags
        #     data.decompose()
        #
        # # List of html tags stripped paragraphs [para1, para2, para3,.....]
        # newData = list(soup.stripped_strings)
        # print(newData)
        # newData = data
        # newData = newData[newData.index('Verbatim')+8:]
        # newData = newData[newData.index('<div>'):]
        # print(newData)

    def getCompList(self):
        count = 0
        # file = open("../inputFiles/compList.txt", "r")
        # compData = file.read()
        # compData = compData.split('\n')
        # print(data)
        # data = [c.split('|')[0] for c in compData]
        lookupDict = {k.strip("\\").replace("&", "and"): 0 for k in self.compData}
        length = len(lookupDict)
        # print(set(data))
        for d in self.compData:
            self.getMacroLink(d.strip("\\").replace("&", "and"))
            # getCompRevenue(d.strip("\"))

        # self.countOfMacroTables = len(self.compRevDict.values())
        print("Number of macrotrend links found: " + str(self.countOfLinks) + "/" + str(length))
        print("Number of Revenue values found within those links: " + str(self.countOfMacroTables) + "/" + str(length))
        print(self.compRevDict)

        print("Companies with incomplete revenues:")
        for (k, v) in self.compRevDict.items():
            if v == -1.0:
                print(k, ":", lookupDict[k])


def getRevenue(compList):
    startTime = time.time()
    obj = getCompRevenue(compList)
    obj.getCompList()
    # obj.getMacroLink("JPMORGAN CHASE and CO")
    # obj.getRevenue("https://www.macrotrends.net/stocks/charts/JPM/jpmorgan-chase/revenue")
    # getCompRevenue('Zoom Video Communications, Inc.')
    # getRevenue('')
    endTime = time.time()
    print(endTime - startTime)
