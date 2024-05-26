
from analyse_phishing.check_url.check_url import CheckURL
from analyse_phishing.extract_url.extract_url import ExtractUrlBalises
from analyse_phishing.extract_logo.extract_logo import ExtractLOGO
from analyse_phishing.extract_certificat.extract_cert import ExtractCert
from analyse_phishing.extract_balises.extract_balises import ExtractBALISES

from analyse_phishing.model.model import Model

class Main:
    
    def __init__(self, url):
        self.url = url

    def main(self, official_sites):

        checkURL = CheckURL(self.url)
        extractURL = ExtractUrlBalises(self.url)
        extractLogo = ExtractLOGO(self.url)
        extractCert = ExtractCert(self.url)
        extractBalises = ExtractBALISES(self.url)

        #Il faut envoyer au model le score en 0 et 1 des analyse de l'url, logo, cert...
        #modelResult = Model(checkURL, extractLogo[1], extractCert[1])
        modelResult = Model("0.90", "0.90", "0.90", "0.90")
        #print("prediction :", modelResult.prediction())

        all_data = {
            "scores":{ "resultModel": modelResult.prediction(),
                    "checkURL": checkURL.url_matching()[1],
                    "extractURL": extractURL.urls_balises_info()[1],
                    "extractLogo": 0.0,#extractLogo.logo_info()[1],
                    "extractCert": extractCert.get_cert_info()[1],
                    "extractTemplate": extractBalises.balises_info()[1],
                    "extractKeyword": 0.0
                    },
            "datas":{
                    "checkURL": checkURL.url_matching()[0],
                    "extractURL": extractURL.urls_balises_info()[0],
                    "extractLogo": "logo",#extractLogo.logo_info()[0],
                    "extractCert": extractCert.get_cert_info()[0],
                    "extractTemplate": extractBalises.balises_info()[0],
                    "extractKeyword": "keyword"
                    }
        }
        return all_data