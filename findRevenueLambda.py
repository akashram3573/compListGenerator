import collections
import boto3
import requests
from bs4 import BeautifulSoup

class getCompRevenue:
    def __init__(self, compList, verticalGroup):
        self.countOfLinks = 0
        self.countOfMacroTables = 0
        self.compRevDict = collections.defaultdict(float)
        self.compData = compList
        self.verticalGroup = verticalGroup

    def getRevenueCategory(self, rev):
        if rev<1.0:
            return "small"
        elif rev>=1 and rev<10:
            return "medium"
        elif rev>=10 and rev<20:
            return "large"
        else:
            return "superLarge"
    def getRevenue(self, mTrendLink):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

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

        for aTag in aTags:
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

    def getCompList(self):

        for d in self.compData:
            self.getMacroLink(d.strip("\\").replace("&", "and"))

        resDict = collections.defaultdict()
        resDict["compList"]=list()
        resDict["verticalName"]=str

        for (k, v) in self.compRevDict.items():
            if v == -1.0:
                # print(k, ":", lookupDict[k])
                continue
            else:
                temp = k+"|"+str(v)+"|"+self.getRevenueCategory(v)
                resDict["compList"].append(temp)
        print(resDict.keys())
        return resDict



def getRevenue(compList, verticalGroup):
    obj = getCompRevenue(compList, verticalGroup)
    resCompCatList = obj.getCompList()
    return resCompCatList