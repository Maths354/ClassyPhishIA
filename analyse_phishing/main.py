
from analyse_phishing.check_url.check_url import CheckURL
from analyse_phishing.extract_url.extract_url import ExtractUrlBalises
from analyse_phishing.extract_logo.extract_logo import ExtractLOGO
from analyse_phishing.extract_certificat.extract_cert import ExtractCert
from analyse_phishing.extract_balises.extract_balises import ExtractBALISES

from analyse_phishing.model.model import Model

class Main:
    
    def __init__(self, url):
        self.url = url

    def main(self):

        checkURL = CheckURL(self.url)
        extractURL = ExtractUrlBalises(self.url)
        extractLogo = ExtractLOGO(self.url)
        extractCert = ExtractCert(self.url)
        extractBalises = ExtractBALISES(self.url)

        #Il faut envoyer au model le score en 0 et 1 des analyse de l'url, logo, cert...
        #modelResult = Model(checkURL, extractLogo[1], extractCert[1])
        modelResult = Model("0.90", "0.90", "0.90", "0.90")
        #print("prediction :", modelResult.prediction())

        all_data = { "resultModel": modelResult.prediction(),
                     "checkURL": checkURL.url_matching(),
                     "extractURL": extractURL.urls_balises_info(),
                     "extractLogo": extractLogo.logo_info(),
                     "extractCert": extractCert.get_cert_info(),
                     "extractTemplate": extractBalises.balises_info(),
                     "extractKeyword": "keyword"
                    }

        return all_data
    
#res = Main("https://google.com")
#data = res.main()
#print("data : ", data)



    