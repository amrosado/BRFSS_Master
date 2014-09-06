__author__ = 'arosado'

import io
import re
import lxml
import pycurl

class SPIRipper:

    #Initalize buffers and parsing objects
    currentBuffer = io.BytesIO()
    curlObject = pycurl.Curl()
    currentCookies = []
    pastCookies = []
    currentHTML = lxml
    currentRE = re

    currentSetId = ''

    # #Urls of interest
    # displayUrl = 'http://apps.nccd.cdc.gov/brfss/display.asp?'
    # selQuesUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/SelQuestion.asp?'
    # quesPageUrl = 'http://apps.nccd.cdc.gov/brfss/page.asp?'
    # listMMSAQuestUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/ListMMSAQuest.asp?'
    # yearsUrl = 'http://apps.nccd.cdc.gov/brfss/years.asp?'
    # SelMMSAPrevDataUrl = 'http://apps.nccd.cdc.gov/BRFSS-SMART/SelMMSAPrevData.asp?'
    # #qkeyDetermineUrl = 'http://apps.nccd.cdc.gov/brfss/display.asp?cat=AC&yr=212&state=US&qkey='
    drugClassesParams = ['drug_class_code', 'drug_class_coding_system', 'class_code_type', 'class_name', 'unii_code']
    drugClassesXMLUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/drugclasses.xml?'
    drugClassesJSONUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/drugclasses.json?'
    drugClassesPharmacologicClassesUrl = 'ftp://ftp1.nci.nih.gov/pub/cacore/EVS/NDF-RT/'
    drugClassesClassCodeTypeParams = ['all', 'epc', 'moa', 'pe', 'ci']


    drugNameParams = ['drug_name', 'name_type', 'manufacturer']
    drugNameNameTypeParams = ['generic', 'brand', 'both']
    drugNamesXMLUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames.xml?'
    drugNamesJSONUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames.json?'

    ndcsXMLUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/ndcs.xml?'
    ndcsJSONUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/rxcuis.json?'

    rxcuisParams = ['rxtty', 'rxstring', 'rxcui']
    rxcuisRxttyParams = ['SBD', 'SCD', 'BPCK', 'GPCK', 'SY']
    rxcuisXMLUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/rxcuis.xml?'
    rxcuisJSONUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/ndcs.json?'

    splsDeaScheduleCodeParams = ['none', 'C48672', 'C48675', 'C48676', 'C48677', 'C48679']

    splsDocTypeDocLabelingContentType = {'53409-9' : 'BULK INGREDIENT',
                                         '60684-8' : 'CELLULAR THERAPY',
                                         '58474-8' : 'COSMETIC',
                                         '58476-3' : 'DIETARY SUPPLEMENT',
                                         '70097-1' : 'ESTABLISHMENT DE-REGISTRATION',
                                         '51725-0' : 'ESTABLISHMENT REGISTRATION',
                                         '71743-9' : 'GENERIC DRUG FACILITY IDENTIFICATION SUBMISSION',
                                         '34390-5' : 'HUMAN OTC DRUG LABEL',
                                         '34391-3' : 'HUMAN PRESCRIPTION DRUG LABEL',
                                         '72090-4' : 'IDENTIFICATION OF CBER-REGULATED GENERIC DRUG FACILITY',
                                         '71446-9' : 'INDEXING - INDICATION',
                                         '63417-0' : 'INDEXING - BILLING UNIT',
                                         '60685-5' : 'INDEXING - PHARMACOLOGIC CLASS',
                                         '64124-1' : 'INDEXING - SUBSTANCE',
                                         '53407-3' : 'LICENSE BLOOD INTERMEDIATES/PASTE LABEL',
                                         '53408-1' : 'LICENSED MINIMALLY MANIPULATED CELLS LABEL',
                                         '53406-5' : 'LICENSED VACCINE BULK INTERMEDIATE LABEL',
                                         '55439-4' : 'MEDICAL DEVICE',
                                         '58475-5' : 'MEDICAL FOOD',
                                         '53410-7' : 'NO CHANGE NOTIFICATION',
                                         '53405-7' : 'NON-STANDARDIZED ALLERGENIC LABEL',
                                         '69968-6' : 'NDC LABELER CODE INACTIVATION',
                                         '72871-7' : 'NDC LABELER CODE REQUEST - ANIMAL DRUG',
                                         '51726-8' : 'NDC/NHRIC LABELER CODE REQUEST',
                                         '50577-6' : 'OTC ANIMAL DRUG LABEL',
                                         '69403-4' : 'OTC MEDICAL DEVICE LABEL',
                                         '50576-8' : 'OTC TYPE A MEDICATED ARTICLE ANIMAL DRUG LABEL',
                                         '50574-3' : 'OTC TYPE B MEDICATED FEED ANIMAL DRUG LABEL',
                                         '50573-5' : 'OTC TYPE C MEDICATED FEED ANIMAL DRUG LABEL',
                                         '53411-5' : 'OUT OF BUSINESS NOTIFICATION',
                                         '60683-0' : 'PLASMA DERIVATIVE',
                                         '50578-4' : 'PRESCRIPTION ANIMAL DRUG LABEL',
                                         '69404-2' : 'PRESCRIPTION MEDICAL DEVICE LABEL',
                                         '60682-2' : 'STANDARDIZED ALLERGENIC',
                                         '53404-0' : 'VACCINE LABEL',
                                         '50575-0' : 'VFD TYPE A MEDICATED ARTICLE ANIMAL DRUG LABEL',
                                         '50572-7' : 'VFD TYPE B MEDICATED FEED ANIMAL DRUG LABEL',
                                         '50571-9' : 'VFD TYPE C MEDICATED FEED ANIMAL DRUG LABEL',}

    splsDrugClassCodingSystemParams = ['2.16.840.1.113883.3.26.1.5']
    splsNameTypeParams = ['generic', 'brand', 'both']
    splsParams = ['application_number', 'dea_schedule_code', 'doctype', 'drug_class_code', 'drug_class_coding_system', 'drug_name', 'name_type', 'labeler', 'manufacturer', 'marketing_category_code', 'ndc', 'rxcui', 'setid', 'unii_code']
    splsXMLUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/spls.xml?'
    splsJSONUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?'

    splsSetIdParams = ['SETID']
    splsSetIdXMLUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/spls/'
    splsSetIdJSONUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/spls/'

    splsHistory = ['SETID']
    splsSetIdHistoryXMLUrl = '/history.xml'
    splsSetIdHistoryJSONUrl = 'history.json'

    splsMediaParamns = ['SETID']
    splsSetIdMediaXMLUrl = '/media.xml'
    splsSetIdMediaJSONUrl = '/media.json'

    splsNdcsParams = ['SETID']
    splsSetIdNdcsXMLUrl = '/ndcs.xml?'
    splsSetIdNdcsJSONUrl = '/ndcs.json?'

    splsPasckingParams = ['SETID']
    splsSetIdPackingXMLUrl = '/packaging.xml?'
    splsSetIdPackingJSONUrl = '/packaging.json?'

    unilsInputParams = ['active_moiety', 'drug_class_code', 'drug_class_coding_system', 'unii_code']
    unilsXMLUrl = '/uniis.xml?'
    unilsJSONUrl = '/uniis.json?'

    applicationNumberInputParams = ['application_number', 'marketing_category_code', 'setid']
    applicationNumberOutputParams = ['pagesize', 'page']
    applicationNumbersJsonUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/applicationnumbers.json?'
    applicationNumbersXMLUrl = 'http://dailymed.nlm.nih.gov/dailymed/services/v2/applicationnumbers.xml?'


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