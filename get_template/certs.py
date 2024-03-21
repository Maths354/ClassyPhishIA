import ssl
import socket

def get_certificate(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
            cert = sslsock.getpeercert()
            return cert

# Exemple d'utilisation :
hostname = "www.zone-telechargement.tokyo/"  # Remplacez par le nom de domaine du site dont vous voulez récupérer le certificat
certificate = get_certificate(hostname)
print(certificate)
