
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

        modelResult = Model(Domain_URL[1], Logo[1], Cert[1], Page_URL[1])
        #modelResult = Model("1.00", "0.80", "0.90")
        #print("prediction :", modelResult.prediction())

        all_data = {
            "scores":{ "resultModel": modelResult.prediction(),
                    "checkURL": Domain_URL[1],
                    "extractURL": Page_URL[1],
                    "extractLogo": Logo[1],
                    "extractCert": Cert[1],
                    "extractKeyword": 0.0,
                    "extractTemplate": Template[1]
                    },
            "datas":{
                    "checkURL": Domain_URL[0],
                    "extractURL": Page_URL[0],
                    "extractLogo": Logo[0],
                    "extractCert": Cert[0],
                    "extractTemplate": Template[0],
                    "extractKeyword": KeyWord,
                    "extractTemplate": Template[0]
                    },
            "id_official":{
                    "checkURL": Domain_URL[2],
                    "extractURL": Page_URL[2],
                    "extractLogo": Logo[2],
                    "extractCert": Cert[2],
                    "extractKeyword": "mettre_site_trouvé",
                    "extractTemplate": Template[2]
                    }
        }
        return all_data
