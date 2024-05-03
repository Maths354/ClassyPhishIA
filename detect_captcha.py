import requests
from bs4 import BeautifulSoup

def check_for_captcha(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        captcha_types = {
            'g-recaptcha': 'Google reCAPTCHA',
            'recaptcha': 'Google reCAPTCHA',
            'h-captcha': 'hCaptcha',
            '__cf_chl_captcha_tk__': 'Cloudflare CAPTCHA',
        }

        for keyword, captcha_type in captcha_types.items():
            if soup.find_all(string=lambda text: keyword in text.lower()):
                return captcha_type
            if soup.find_all(True, {'class': lambda x: x and keyword in x.lower()}):
                return captcha_type
            if soup.find_all(True, {'id': lambda x: x and keyword in x.lower()}):
                return captcha_type

        return "Aucun CAPTCHA détecté"
    
    except requests.RequestException as e:
        print(f"Une erreur est survenue lors de la récupération de l'URL: {e}")
        return "Erreur lors de la vérification"

#url_to_check = "https://www.deepl.com/fr/translator"
url_to_check = "https://douaclaud.info/"

captcha_type = check_for_captcha(url_to_check)
print(f"Résultat: {captcha_type}")
