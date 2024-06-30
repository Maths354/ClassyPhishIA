
from inject_db.extract_url.extract_url import ExtractUrlBalises
from inject_db.extract_logo.extract_logo import ExtractLOGO
from inject_db.extract_certificat.extract_cert import ExtractCert
from inject_db.extract_balises.extract_balises import ExtractBALISES
from inject_db.extract_key_word.extract_key_word import ExtractKeyWord

class Main:
    
    def __init__(self, url):
        self.url = url

    def main(self):

        extractURL = ExtractUrlBalises(self.url)
        extractLogo = ExtractLOGO(self.url)
        extractCert = ExtractCert(self.url)
        extractBalises = ExtractBALISES(self.url)
        extractKeyWord = ExtractKeyWord(self.url)


        Page_URL=extractURL.urls_balises_info()
        Logo=extractLogo.logo_info()
        Cert=extractCert.get_cert_info()
        Template=extractBalises.balises_info()
        KeyWord=extractKeyWord.extract_domain()

        all_data = {
            "datas":{
                    "extractURL": Page_URL,
                    "extractLogo": Logo,
                    "extractCert": Cert,
                    "extractTemplate": Template,
                    "extractKeyword": KeyWord
                    },
        }
        return all_data