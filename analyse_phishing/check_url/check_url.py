
import difflib


class CheckURL:
    
    def __init__(self, url):
        self.url = url

    def url_matching(self):

        domain = self.url.split("/")[2]

        companies=["www.orange.fr","abc.rouge.fr","www.bleu.com"]
        top_ratio=0
        top_string=""

        for company in companies:
            company_str_len=len(company)
            for start_letter in range(company_str_len):
                for end_letter in range(start_letter,company_str_len):
                    ratio=difflib.SequenceMatcher(None, domain, company[start_letter:end_letter+1]).ratio()
                    if ratio>top_ratio:
                        top_ratio=ratio
                        top_string=company[start_letter:end_letter+1]

        print("test1 : ", top_ratio, " ", top_string)
        return top_ratio, top_string