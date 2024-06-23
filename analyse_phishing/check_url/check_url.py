
import difflib

class CheckURL:
    
    def __init__(self, url, official_sites):
        self.url = url
        self.official_sites = official_sites

    def url_matching(self):
        top_ratio=0
        top_string=""
        top_company=""

        for company in self.official_sites:
            company_url = company["url"]
            company_str_len=len(company_url)
            for start_letter in range(company_str_len):
                for end_letter in range(start_letter,company_str_len):
                    ratio=difflib.SequenceMatcher(None, self.url, company_url[start_letter:end_letter+1]).ratio()
                    if ratio>top_ratio:
                        top_ratio=ratio
                        top_string=company_url[start_letter:end_letter+1]
                        top_company=[company["id"],company["url"]]

        return top_string, float("%.3f" % top_ratio), top_company