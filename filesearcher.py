import pandas as pd
from cosineSimilarity import getComp1
from editDistance import getComp2
from findRevenue import getRevenue
class comp_list_generator:
    def __init__(self):
        self.unique_company_index = []
        self.company_list = []
        self.index_df = pd.DataFrame()
        self.output_company_list = []
        self.not_captured_companies = []

    def preprocess(self, company):
        new_comp = ""
        company = company.lower()
        if "," in company:
            company = company.replace(",", "")
        if "." in company:
            company = company.replace(".", "")
        if "!" in company:
            company = company.replace("!", "")
        if "the " in company[:5]:
            company = company.replace("the ", "")

        # if "-" in company:
        #     company=company.replace("-"," ")
        if "\n" in company:
            company = company.strip('\n')
        if " incorporated" in company[-len(" incorporated"):]:
            company = company.replace(" incorporated", "")
        if " inc" in company[-len(" inc"):]:
            company = company.replace(" inc", "")
        if " company" in company[-len(" company"):]:
            company = company.replace(" company", "")
        if " corporation" in company[-len(" corporation"):]:
            company = company.replace(" corporation", "")
        if " corporated" in company[-len(" corporated"):]:
            company = company.replace(" corporated", "")
        if " corp" in company[-len(" corp"):]:
            company = company.replace(" corp", "")
        if " co" in company[-len(" co"):]:
            company = company.replace(" co", "")
        if " limited" in company[-len(" limited"):]:
            company = company.replace(" limited", "")
        if " ltd" in company[-len(" ltd"):]:
            company = company.replace(" ltd", "")
        new_comp = company
        return new_comp

    def read_files(self):
        self.index_df = pd.read_csv("./compFiles/qtr1_2023.idx", sep="|")
        self.index_df = self.index_df.drop_duplicates(subset="Company Name")
        self.index_df["Company_Name_Initial"] = self.index_df["Company Name"]
        self.index_df["Company Name"] = self.index_df["Company Name"].apply(self.preprocess)

        company_index = self.index_df["Company Name"].values

        self.unique_company_index = list(set(company_index))

        # company_list = pd.read_csv("nasdaq100_companies.txt", sep="\\n")

        f = open("./compFiles/snp_500_customers.txt", "r")
        self.company_list = []
        for x in f:
            self.company_list.append(x)

    def comp_list(self):
        self.output_company_list=[]
        #Dataframe approach
        i=0
        self.not_captured_companies=[]
        print(len(self.company_list))
        for company in self.company_list:
            comp=self.preprocess(company)
            new_df=self.index_df[self.index_df["Company Name"].str.contains(comp)]
            lookupDict = pd.Series(new_df.Company_Name_Initial.values, index = new_df["Company Name"]).to_dict()
            if len(new_df)==0:
                if "-" in comp:
                    comp=comp.replace("-"," ")
                    new_df=self.index_df[self.index_df["Company Name"].str.contains(comp)]
                    if len(new_df)==0:
                        self.not_captured_companies.append(comp)
                        i+=1
                elif "'" in comp:
                    new_comp=comp.replace("'"," ")
                    new_df=self.index_df[self.index_df["Company Name"].str.contains(new_comp)]
                    if len(new_df)==0:
                        new_comp_2=comp.replace("'","")
                        new_df=self.index_df[self.index_df["Company Name"].str.contains(new_comp_2)]
                        if len(new_df)==0:
                            self.not_captured_companies.append(comp)
                            i+=1
                else:
                    self.not_captured_companies.append(comp)
                    i+=1
            new_df["Company_Name_Original"] = new_df["Company Name"].map(lookupDict)

            index_list=new_df["Company_Name_Original"].values
            # print(index_list, company, comp)
            # index_list = set(getComp1(index_list, company)).intersection(getComp2(index_list, company))
            index_list = getComp2(index_list, company)
            for ind in index_list:
                if ind not in self.output_company_list:
                    self.output_company_list.append(ind)

        # print(self.output_company_list)
        # print(len(self.output_company_list))
        # print("self.not_captured_companies:",self.not_captured_companies)
        # print(len(self.not_captured_companies))

    def gen_comp_list(self):
        self.read_files()
        self.comp_list()
        return self.output_company_list, self.not_captured_companies

def getAccuracy(output_comp_list):
    file = open("./compFiles/snp_500_customers.txt","r")
    data = list()
    count = 0
    for d in file:
        data.append(d.strip("\n"))
    for d in data:
        if d not in output_comp_list:
            print(d)
            count += 1
    print(count)

if __name__=="__main__":
    obj = comp_list_generator()
    output_comp_list, not_captured_company = obj.gen_comp_list()
    # print(output_comp_list)
    # print(not_captured_company)
    # print(len(set(output_comp_list)))
    # print(len(output_comp_list))
    getRevenue(set(output_comp_list))
    # getAccuracy(output_comp_list)