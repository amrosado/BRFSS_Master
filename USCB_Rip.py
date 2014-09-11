__author__ = 'arosado'

import io
import re
import lxml
import pycurl
import json
import pickle
import collections

class USCBRipper:

    #Initalize buffers and parsing objects
    currentBuffer = io.BytesIO()
    curlObject = pycurl.Curl()
    currentCookies = []
    pastCookies = []
    currentHTML = lxml
    currentRE = re
    currentJson = {}

    # #Urls of interest
    # displayUrl = 'http://apps.nccd.cdc.gov/brfss/display.asp?'
    # selQuesUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/SelQuestion.asp?'
    # quesPageUrl = 'http://apps.nccd.cdc.gov/brfss/page.asp?'
    # listMMSAQuestUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/ListMMSAQuest.asp?'
    # yearsUrl = 'http://apps.nccd.cdc.gov/brfss/years.asp?'
    # SelMMSAPrevDataUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/SelMMSAPrevData.asp?'
    # #qkeyDetermineUrl = 'http://apps.nccd.cdc.gov/brfss/display.asp?cat=AC&yr=2012&state=US&qkey='

    USCBUrl = 'http://api.census.gov/data/'
    USCBYears = ['1990', '2000', '2007', '2010', '2011', '2012', '2013']
    USCBKey = "daaba7a1a566a8cb884ef6b042e232b7a42d2b33"

    jsonLoadAll = []
    webServiceUrls = []
    apiYearsJson = []
    apiUrlComponents = []
    apiUrlCalls = []
    apiVariablesJson = []
    apiVariables = []
    apiGeographyJson = []
    apiGeography = []



    # def iterqkey(self):
    #     i = 0
    #     while(i < 10000):
    #         iterUrl = self.qkeyDetermineUrl + str(i)
    #         self.selectBRFSSUrl(iterUrl)
    #         self.returnCurrentBrfssUrlHTML()
    def loadAllPastApiPickles(self):
        self.apiYearsJson = pickle.load(open('apiYearsJson.pickle', 'rb'))
        self.apiUrlComponents = pickle.load(open('apiUrlComponents.pickle', 'rb'))
        self.apiVariablesJson = pickle.load(open('apiVariablesJson.pickle', 'rb'))
        self.apiVariables = pickle.load(open('apiVariables.pickle', 'rb'))
        self.apiGeographyJson = pickle.load(open('apiGeographyJson.pickle', 'rb'))
        self.apiGeography = pickle.load(open('apiGeography.pickle', 'rb'))

    def buildUrlCallsForServices(self):
        for i in self.apiUrlComponents:
            currentUrl = i['services'][0]+self.USCBKey
            for k in self.apiVariables:
                if ((k['datasetName'] == i['dataset']) and (k['year'] == i['year'])):
                    pass




    def propagateServiceData(self):
        pass

    def propagateUSCBServices(self):
        for i in self.apiYearsJson:
            selectedJson = i[1]
            for k in selectedJson:
                self.apiUrlComponents.append({'year' : i[0] , 'dataset' : [k['c_dataset']], 'variables' : [k['c_variablesLink']] , 'geography' : [k['c_geographyLink']], 'tags' : ['c_tagsLink'], 'services' : [k['webService']]})
        file = open('apiUrlComponents.pickle', 'wb')
        pickle.dump(self.apiUrlComponents, file)


    def propagateVariables(self):
        serviceVariables = []
        for i in self.apiUrlComponents:
            variableJsonBytes = self.curlUrl(i['variables'][0])
            variableJsonString = variableJsonBytes.decode('UTF-8', 'replace')
            variableJson = json.loads(variableJsonString)
            variableYear = i['year']
            self.apiVariablesJson.append([i['dataset'] , variableYear, variableJson])
        file = open('apiVariablesJson.pickle', 'wb')
        pickle.dump(self.apiVariablesJson, file)
        for k in self.apiVariablesJson:
            for j in k[2]['variables']:
                serviceVariables.append({'variable' : j})
            self.apiVariables.append({'datasetName' : k[0], 'year': k[1],'variables' : serviceVariables})
            serviceVariables = []
        file2 = open('apiVariables.pickle', 'wb')
        pickle.dump(self.apiVariables, file2)


    def propagateGeography(self):
        serviceGeography = []
        for i in self.apiUrlComponents:
            geographyJsonBytes = self.curlUrl(i['geography'][0])
            geographyJsonString = geographyJsonBytes.decode('UTF-8', 'replace')
            geographyJson = json.loads(geographyJsonString)
            geographyYear = i['year']
            self.apiGeographyJson.append([i['dataset'] , geographyYear, geographyJson])
        file = open('apiGeographyJson.pickle', 'wb')
        pickle.dump(self.apiUrlComponents, file)

        for k in self.apiGeographyJson:
            geographyDic = k[2]
            if 'fips' in geographyDic:
                for j in geographyDic['fips']:
                    serviceGeography.append({'fips' : j})
            if 'default' in geographyDic:
                for j in geographyDic['default']:
                    serviceGeography.append({'default' : j})
            self.apiGeography.append({'datasetName' : k[0], 'year': k[1],'geography' : serviceGeography})
            serviceGeography = []
        file2 = open('apiGeography.pickle', 'wb')
        pickle.dump(self.apiGeography, file2)




    def storeAllYearsJson(self):
        for i in self.USCBYears:
            yearUrl = self.USCBUrl + i
            curlBytes = self.curlUrl(yearUrl)
            curlString = curlBytes.decode('UTF-8', 'replace')
            curlJsonEncoded = json.loads(curlString)
            self.apiYearsJson.append([i, curlJsonEncoded])
        file = open('apiYearsJson.pickle', 'wb')
        pickle.dump(self.apiYearsJson, file)

    def grabCurrentBRFSSInformation(self):
        pass

    #Configures curl object for new url to write to object buffer
    def curlUrl(self, url):
        temporaryBuffer = io.BytesIO()

        self.curlObject.setopt(pycurl.URL, url)
        self.curlObject.setopt(pycurl.HTTPHEADER, ["Accept:"])
        self.curlObject.setopt(pycurl.WRITEFUNCTION, temporaryBuffer.write)
        self.curlObject.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curlObject.setopt(pycurl.MAXREDIRS, 10)
        self.curlObject.setopt(pycurl.COOKIEFILE, 'cookie.txt')

        self.currentCookies = self.curlObject.getinfo(pycurl.INFO_COOKIELIST)

        self.curlObject.perform()

        return temporaryBuffer.getvalue()

    def __init__(self):
        pass

uscbParser = USCBRipper()
#uscbParser.storeAllYearsJson()
#uscbParser.propagateUSCBServices()
#uscbParser.propagateVariables()
#uscbParser.propagateGeography()
#uscbParser.propagateServiceData()

uscbParser.loadAllPastApiPickles()
uscbParser.buildUrlCallsForServices()

test = uscbParser