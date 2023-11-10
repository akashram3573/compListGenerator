import json
import boto3
import pandas as pd
from editDistance import getComp2
from findRevenueLambda import getRevenue

import sys
sys.path.append('C:\persistent\SalesFI_project\secCrawlerMain')
from salesfi_p1_index_lookup.indexParser import indexParser


class comp_list_generator:
    def __init__(self, compList):
        self.unique_company_index = []
        self.company_list = compList
        self.index_df = pd.DataFrame()
        self.output_company_list = []
        self.not_captured_companies = []

    # Pre-processing function to simplify company names
    def preprocess(self, company):
        # Initialize dummy variable new_comp
        new_comp = ""

        # Convert to lower case
        company = company.lower()

        # Strip '\','\n' which might precede/supersede company names and thus lead to errors
        company = company.strip('\\')
        company = company.strip('\n')

        # Check for [',','.','!','the '] and replace these with empty characters
        if "," in company:
            company = company.replace(",", "")
        if "." in company:
            company = company.replace(".", "")
        if "!" in company:
            company = company.replace("!", "")
        if "-" in company[:5]:
            company = company.replace("-", "")
        if "the " in company[:5]:
            company = company.replace("the ", "")

        # Check for presence of common company and replace with empty character
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
        self.index_df = pd.read_csv("../qtr1_2023.idx", sep="|")
        self.index_df = self.index_df.drop_duplicates(subset="Company Name")
        self.index_df["Company_Name_Initial"] = self.index_df["Company Name"]
        self.index_df["Company Name"] = self.index_df["Company Name"].apply(self.preprocess)
        company_index = self.index_df["Company Name"].values
        self.unique_company_index = list(set(company_index))


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
            index_list = getComp2(index_list, company)
            for ind in index_list:
                if ind not in self.output_company_list:
                    self.output_company_list.append(ind)

    def gen_comp_list(self):
        self.read_files()
        self.comp_list()
        return self.output_company_list, self.not_captured_companies

def getAccuracy(output_comp_list):
    file = open("./compFiles/input_files.txt","r")
    data = list()
    count = 0
    for d in file:
        data.append(d.strip("\n"))
    for d in data:
        if d not in output_comp_list:
            print(d)
            count += 1
    print(count)

def writeFile(resDict, fileName='compList.json'):
    # Code to write to s3 bucket
    resDict = json.dumps(resDict)
    s3 = boto3.resource('s3')
    s3Obj = s3.Object('sec-corpus',fileName)
    s3Obj.put(resDict)

    # Code to call subsequent lambda function call
    # lambdaClient = boto3.client('lambda', region_name='us-east-1')
    # res = lambdaClient.invoke(FunctionName="indexParser", InvocationType="Event",
    #                           Payload=json.dumps({'res': json.dumps(resDict)}))

    return

# def fileSearcher(event, context):
def fileSearcher():
    filename = "../compFiles/input_files.txt"
    verticalGroup = "sample1"

    file = open(filename,'r')
    compList = file.readlines()
    compList = [comp.strip('\n') for comp in compList]
    # compList = data.split('\n')
    # compList=['ross stores', 'starbucks', 'seagen', 'sirius xm holdings', 'synopsys', 'splunk', 'skyworks solutions']
    # print(compList)

    obj = comp_list_generator(compList)
    output_comp_list, not_captured_company = obj.gen_comp_list()

    resCompCatList = getRevenue(set(output_comp_list), verticalGroup)

    resCompCatList['verticalName'] = verticalGroup
    print(resCompCatList)
    # indexParser(resCompCatList)
    print(len(resCompCatList['compList']))
    getAccuracy(output_comp_list)

fileSearcher()