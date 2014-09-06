__author__ = 'arosado'

import io
import re
import lxml
import pycurl

class USCBRipper:

    #Initalize buffers and parsing objects
    currentBuffer = io.BytesIO()
    curlObject = pycurl.Curl()
    currentCookies = []
    pastCookies = []
    currentHTML = lxml
    currentRE = re

    # #Urls of interest
    # displayUrl = 'http://apps.nccd.cdc.gov/brfss/display.asp?'
    # selQuesUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/SelQuestion.asp?'
    # quesPageUrl = 'http://apps.nccd.cdc.gov/brfss/page.asp?'
    # listMMSAQuestUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/ListMMSAQuest.asp?'
    # yearsUrl = 'http://apps.nccd.cdc.gov/brfss/years.asp?'
    # SelMMSAPrevDataUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/SelMMSAPrevData.asp?'
    # #qkeyDetermineUrl = 'http://apps.nccd.cdc.gov/brfss/display.asp?cat=AC&yr=2012&state=US&qkey='

    USCBUrl = 'http://api.census.gov/data/'
    USCBYears = []


    # def iterqkey(self):
    #     i = 0
    #     while(i < 10000):
    #         iterUrl = self.qkeyDetermineUrl + str(i)
    #         self.selectBRFSSUrl(iterUrl)
    #         self.returnCurrentBrfssUrlHTML()

    def returnCurrentBrfssUrlHTML(self):
        self.curlObject.perform()
        return self.currentBuffer.getbuffer()

    def grabCurrentBRFSSInformation(self):
        pass

    #Configures curl object for new url to write to object buffer
    def selectBRFSSUrl(self, brfssUrl):
        self.curlObject.setopt(pycurl.URL, brfssUrl)
        self.curlObject.setopt(pycurl.HTTPHEADER, ["Accept:"])
        self.curlObject.setopt(pycurl.WRITEFUNCTION, self.currentBuffer.write)
        self.curlObject.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curlObject.setopt(pycurl.MAXREDIRS, 10)
        self.curlObject.setopt(pycurl.COOKIEFILE, 'cookie.txt')

        self.currentCookies = self.curlObject.getinfo(pycurl.INFO_COOKIELIST)

    def __init__(self):
        pass