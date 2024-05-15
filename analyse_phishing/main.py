
from analyse_phishing.check_url.check_url import CheckURL
from analyse_phishing.extract_url.extract_url import ExtractURL
from analyse_phishing.extract_logo.extract_logo import ExtractLogo
from analyse_phishing.extract_certificat.extract_cert import ExtractCert

class Main:
    
    def __init__(self, url):
        self.url = url

    def main(self):

        checkURL = CheckURL(self.url)
        extractURL = ExtractURL(self.url)
        extractLogo = ExtractLogo(self.url)
        extractCert = ExtractCert(self.url)

        all_data = { "checkURL": checkURL.url_matching(),
                     "extractURL": extractURL.extract_and_save_urls(),
                     "extractLogo": extractLogo.extract_logo_url(),
                     "extractCert": extractCert.get_cert_info() }

        return all_data


    