# Importez les fonctions nécessaires de get_template et get_logo
from get_template.get_template import process_html, parse_html_string, url_input
from get_logo.get_logo import logo_input

# Les URLs légitimes et de phishing
url2 = 'https://www.keraunos.org/'
url1 = 'https://messagerie-mobile-orange.click-app.icu/'

# Obtenir les balises HTML des URLs

# Appeler url_input avec les URLs
enter_template = url_input(url1, url2)

# Appeler logo_input avec les URLs et les balises HTML extraites
enter_logo = logo_input(url1, url2)