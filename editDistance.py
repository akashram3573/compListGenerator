import collections


class editDistanceClass:
    def __init__(self, compList, rootComp):
        self.minDict = collections.defaultdict(int)
        self.compList = compList
        self.rootComp = rootComp
        self.k = 2

    def editDistance(self, s1, s2):
        temp = s1
        s1 = s1.lower()
        l1 = len(s1)
        l2 = len(s2)

        M = [[0 for i in range(l2+1)]for j in range(l1+1)]
        M[0][0] = 0
        for i in range(l1+1):
            M[i][0] = i
        for j in range(l2+1):
            M[0][j] = j
        # print(l1,l2)
        for i in range(1, l1+1):
            for j in range(1, l2+1):
                # print(i,j)
                val = 0 if s1[i-1]==s2[j-1] else 1
                val = M[i-1][j-1] + val
                M[i][j] = min(val, M[i-1][j]+1, M[i][j-1]+1)
        self.minDict[temp] = M[-1][-1]
        # print(M[-1][-1], s1)

    def getMinDistance(self):
        # print("hi")
        for c in self.compList:
            # print(c, self.rootComp)
            self.editDistance(c, self.rootComp)

        minVal = sorted(self.minDict.items(), key=lambda x: x[1])
        res = [k for k,v in minVal[:self.k]]
        # print(res)
        return res


def getComp2(compList=list(), rootComp=""):
    # compList = ['blackrock allocation target shares',
    #             'biotech target n v',
    #             'techtarget inc' 'putnam target date funds',
    #             'american funds target date retirement series',
    #             'blackrock municipal 2030 target term trust',
    #             'american funds college target date series',
    #             'destra targeted income unit investment trust',
    #             'target group inc.',
    #             'bny mellon alcentra global credit income 2024 target term fund, inc.',
    #             'invesco high income 2023 target term fund',
    #             'nuveen credit opportunities 2022 target term fund',
    #             'invesco high income 2024 target term fund',
    #             'virtus convertible & income 2024 target term fund',
    #             'nuveen emerging markets debt 2022 target term fund',
    #             'target hospitality corp.',
    #             'jjm fund (a series of global endowment targeted strategy fund, lp)',
    #             'jjm fund ii (a series of global endowment targeted strategy fund, lp)',
    #             'nuveen corporate income 2023 target term fund',
    #             'aviva investors multi-strategy target return fund',
    #             'man funds xi spc, on behalf of & for the account of man ahl targetrisk 1.5x (cayman) sp',
    #             'periscope target return fund lp',
    #             'blackrock 2037 municipal target term trust',
    #             'tax-free high grade portfolio target maturity fund for puerto rico residents, inc.',
    #             'target global acquisition i corp.',
    #             'tax free target maturity fund for puerto rico residents, inc.',
    #             '2021 targeted portfolio fund llc',
    #             'vhs fund, a series of global endowment targeted strategy fund, lp',
    #             'target global early stage fund iii lp',
    #             'target global selected opportunities, llc - series nickel 2',
    #             'target global selected opportunities, llc - series mercury no 1',
    #             'target global selected opportunities, llc - series vintage i (ex. calcium 2)',
    #             'target global selected opportunities, llc - series vintage ii (ex. palladium 2)',
    #             'target global selected opportunities, llc - series vintage iii',
    #             'target global selected opportunities, llc - series vintage iv',
    #             'target global selected opportunities, llc - series vintage v',
    #             'target global selected opportunities, llc - series mendelevium',
    #             'target global selected opportunities, llc - series lutetium no 4',
    #             'target global selected opportunities, llc - series lutetium no 3',
    #             'target global selected opportunities, llc - series zinc',
    #             'target global selected opportunities, llc - series branded investors',
    #             'target global selected opportunities, llc - series fluorine no 3',
    #             'target global selected opportunities, llc - series fluorine no 4',
    #             'target global selected opportunities, llc - series nickel',
    #             'target global selected opportunities, llc - series rubidium 4',
    #             'target global selected opportunities, llc - series molybdenum',
    #             'target corp',
    #             'american century target maturities trust',
    #             'target portfolio trust',
    #             'blackrock allocation target shares']
    #
    # rootComp = "target"
    # print(compList)
    rootComp = rootComp.lower()
    obj = editDistanceClass(compList, rootComp)
    res = obj.getMinDistance()
    return res

# getComp2()
# minVal = 1000
# minKey = ""
# for k,v in minDict.items():
#     if v < minVal:
#         minVal = v
#         minKey = k
        # print(minKey, minVal)
# print(minDict)
# print(minKey, minVal)

# editDistance("target corp","target corp")