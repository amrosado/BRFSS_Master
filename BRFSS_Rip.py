__author__ = 'arosado'
import pycurl
import io
import re
import lxml

class BRFSSripper:
    currentBuffer = io.BytesIO()
    curlObject = pycurl.Curl()
    currentCookies = []
    pastCookies = []
    currentHTML = lxml
    currentRE = re
    first

    def returnCurrentBrfssUrlHTML(self):
        self.curlObject.perform()


        return

    def grabCurrentBRFSSInformation(self):
        pass

    def selectBRFSSUrl(self, brfssUrl):
        self.curlObject.setopt(pycurl.URL, brfssUrl)
        self.curlObject.setopt(pycurl.HTTPHEADE, ["Accept:"])
        self.curlObject.setopt(pycurl.WRITEFUNCTION, self.currentBuffer.write)
        self.curlObject.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curlObject.setopt(pycurl.MAXREDIRS, 10)
        self.curlObject.setopt(pycurl.COOKIEFILE, 'cookie.txt')

        self.currentCookies = self.curlObject.getinfo(pycurl.INFO_COOKIELIST)

    def __init__(self):
        pass
