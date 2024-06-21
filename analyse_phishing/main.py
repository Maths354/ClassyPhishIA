
from analyse_phishing.check_url.check_url import CheckURL
from analyse_phishing.extract_url.extract_url import ExtractUrlBalises
from analyse_phishing.extract_logo.extract_logo import ExtractLOGO
from analyse_phishing.extract_certificat.extract_cert import ExtractCert
from analyse_phishing.extract_balises.extract_balises import ExtractBALISES
from analyse_phishing.extract_key_word.extract_key_word import ExtractKeyWord

from analyse_phishing.model.model import Model

class Main:
    
    def __init__(self, url):
        self.url = url

    def main(self, official_sites):

        checkURL = CheckURL(self.url, official_sites)
        extractURL = ExtractUrlBalises(self.url, official_sites)
        extractLogo = ExtractLOGO(self.url, official_sites)
        extractCert = ExtractCert(self.url, official_sites)
        extractBalises = ExtractBALISES(self.url, official_sites)
        extractKeyWord = ExtractKeyWord(self.url)

        Domain_URL=checkURL.url_matching()
        Page_URL=extractURL.urls_balises_info()
        Logo=extractLogo.logo_info()
        Cert=extractCert.get_cert_info()
        Template=extractBalises.balises_info()
        KeyWord=extractKeyWord.analyze_text()

        # IMPORTANT :  Mettre dans le Model que la partie score qui sont [1]
        #Il faut envoyer au model le score en 0 et 1 des analyse de l'url, logo, cert...
        #modelResult = Model(checkURL, extractLogo[1], extractCert[1])

        modelResult = Model(Domain_URL[1], Logo[1], Cert[1])
        #modelResult = Model("1.00", "0.80", "0.90")

        #print("prediction :", modelResult.prediction())

        all_data = {
            "scores":{ "resultModel": modelResult.prediction(),
                    "checkURL": Domain_URL[1],
                    "extractURL": Page_URL[1],
                    "extractLogo": Logo[1],
                    "extractCert": Cert[1],
                    "extractKeyword": 0.0
                    },
            "datas":{
                    "checkURL": Domain_URL[0],
                    "extractURL": Page_URL[0],
                    "extractLogo": Logo[0],
                    "extractCert": Cert[0],
                    "extractTemplate": Template[0],
                    "extractKeyword": KeyWord
                    },
            "id_official":{
                    "checkURL": Domain_URL[2],
                    "extractURL": Page_URL[2],
                    "extractLogo": Logo[2],
                    "extractCert": Cert[2],
                    "extractKeyword": "mettre_site_trouvé"
                    }
        }
        return all_data
