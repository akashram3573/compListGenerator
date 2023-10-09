import pandas as pd
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
        if " incorporated" in company:
            company = company.replace(" incorporated", "")
        if " inc" in company:
            company = company.replace(" inc", "")
        if " company" in company:
            company = company.replace(" company", "")
        if " corporation" in company:
            company = company.replace(" corporation", "")
        if " corporated" in company:
            company = company.replace(" corporated", "")
        if " corp" in company:
            company = company.replace(" corp", "")
        if " co" in company[-4:]:
            company = company.replace(" co", "")
        if " limited" in company:
            company = company.replace(" limited", "")
        if " ltd" in company:
            company = company.replace(" ltd", "")
        new_comp = company
        return new_comp

    def read_files(self):
        self.index_df = pd.read_csv("./compFiles/qtr1_2023.idx", sep="|")
        self.index_df = self.index_df.drop_duplicates(subset="Company Name")
        self.index_df["Company Name"] = self.index_df["Company Name"].str.lower()
        print(self.index_df.head())
        company_index = self.index_df["Company Name"].values
        # print(len(company_index))
        self.unique_company_index = list(set(company_index))
        # print(len(unique_company_index))

        # company_list = pd.read_csv("nasdaq100_companies.txt", sep="\\n")

        f = open("./compFiles/snp_500_customers.txt", "r")
        i = 0
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
            # print(comp)
            new_df=self.index_df[self.index_df["Company Name"].str.contains(comp)]
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
            # print(new_df)
            index_list=new_df["Company Name"].values
            print(index_list, company)
            for ind in index_list:
                if ind not in self.output_company_list:
                    self.output_company_list.append(ind)

        print(self.output_company_list)
        print(len(self.output_company_list))
        print("self.not_captured_companies:",self.not_captured_companies)
        print(len(self.not_captured_companies))

    def gen_comp_list(self):
        self.read_files()
        self.comp_list()
        return self.output_company_list, self.not_captured_companies


if __name__=="__main__":
    obj = comp_list_generator()
    output_comp_list, not_captured_company = obj.gen_comp_list()
    print(output_comp_list)
    print(not_captured_company)
    print(len(set(output_comp_list)))
    print(len(output_comp_list))
    # getRevenue(set(output_comp_list))