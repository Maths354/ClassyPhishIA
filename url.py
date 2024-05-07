#pip install cdifflib
import difflib

url="www.0rahge.fr"
companies=["www.orange.fr","rouge","bleu"]
top_ratio=0
top_string=""

for company in companies:
    company_str_len=len(company)
    for start_letter in range(company_str_len):
        for end_letter in range(start_letter,company_str_len):
            ratio=difflib.SequenceMatcher(None, url, company[start_letter:end_letter+1]).ratio()
            if ratio>top_ratio:
                top_ratio=ratio
                top_string=company[start_letter:end_letter+1]

print(top_ratio)
print(top_string)
