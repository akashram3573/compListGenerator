import collections
from collections import Counter
import math

class cosineSimilarity:
    def __init__(self, compList, rootComp):
        self.compList = compList
        self.rootComp = rootComp
        self.resComp = collections.defaultdict(float)

    def findNumerator(self, c1, c2):
        check = set(c1.keys()).intersection(set(c2.keys()))
        numerator = sum([c1[c]*c2[c] for c in check])
        return numerator

    # def cosineSimilarity(self, w1,w2):
    #     c1 = Counter(w1)
    #     c2 = Counter(w2)
    #     sq1 = math.sqrt(sum([c*c for c in c1.values()]))
    #     sq2 = math.sqrt(sum([c*c for c in c2.values()]))
    #     numerator = self.findNumerator(c1,c2)
    #     cosSim = float(numerator/(sq1*sq2))
    #     self.resComp[w1]=cosSim
    #     print(self.resComp)
    #
    def cosineSimilarity(self, w1,w2):
        c1 = Counter(w1.split(" "))
        c2 = Counter(w2.split(" "))
        print(c1,c2)
        sq1 = math.sqrt(sum([c*c for c in c1.values()]))
        sq2 = math.sqrt(sum([c*c for c in c2.values()]))
        numerator = self.findNumerator(c1,c2)
        print(numerator)
        cosSim = float(numerator/(sq1*sq2))
        self.resComp[w1]=cosSim
        print(self.resComp)

    def getMinCosine(self):
        # print(self.compList)
        for c in self.compList:
            print(c, self.rootComp)
            self.cosineSimilarity(c, self.rootComp)
            # break

        self.resComp = sorted(self.resComp.items(), key=lambda x:(-x[1]))
        print(self.resComp[:3])


def getComp(compList=list(), parentComp=""):
    compList = ['blackrock allocation target shares',
                'biotech target n v',
                'techtarget inc' 'putnam target date funds',
                'american funds target date retirement series',
                'blackrock municipal 2030 target term trust',
                'american funds college target date series',
                'destra targeted income unit investment trust',
                'target group inc.',
                'bny mellon alcentra global credit income 2024 target term fund, inc.',
                'invesco high income 2023 target term fund',
                'nuveen credit opportunities 2022 target term fund',
                'invesco high income 2024 target term fund',
                'virtus convertible & income 2024 target term fund',
                'nuveen emerging markets debt 2022 target term fund',
                'target hospitality corp.',
                'jjm fund (a series of global endowment targeted strategy fund, lp)',
                'jjm fund ii (a series of global endowment targeted strategy fund, lp)',
                'nuveen corporate income 2023 target term fund',
                'aviva investors multi-strategy target return fund',
                'man funds xi spc, on behalf of & for the account of man ahl targetrisk 1.5x (cayman) sp',
                'periscope target return fund lp',
                'blackrock 2037 municipal target term trust',
                'tax-free high grade portfolio target maturity fund for puerto rico residents, inc.',
                'target global acquisition i corp.',
                'tax free target maturity fund for puerto rico residents, inc.',
                '2021 targeted portfolio fund llc',
                'vhs fund, a series of global endowment targeted strategy fund, lp',
                'target global early stage fund iii lp',
                'target global selected opportunities, llc - series nickel 2',
                'target global selected opportunities, llc - series mercury no 1',
                'target global selected opportunities, llc - series vintage i (ex. calcium 2)',
                'target global selected opportunities, llc - series vintage ii (ex. palladium 2)',
                'target global selected opportunities, llc - series vintage iii',
                'target global selected opportunities, llc - series vintage iv',
                'target global selected opportunities, llc - series vintage v',
                'target global selected opportunities, llc - series mendelevium',
                'target global selected opportunities, llc - series lutetium no 4',
                'target global selected opportunities, llc - series lutetium no 3',
                'target global selected opportunities, llc - series zinc',
                'target global selected opportunities, llc - series branded investors',
                'target global selected opportunities, llc - series fluorine no 3',
                'target global selected opportunities, llc - series fluorine no 4',
                'target global selected opportunities, llc - series nickel',
                'target global selected opportunities, llc - series rubidium 4',
                'target global selected opportunities, llc - series molybdenum',
                'target corp',
                'american century target maturities trust',
                'target portfolio trust',
                'blackrock allocation target shares']

    rootComp = "target corp"
    # print(compList)
    obj = cosineSimilarity(compList, rootComp)
    # print(obj.compList)
    obj.getMinCosine()
    return

getComp()

