import cv2

# Charger l'image
image = cv2.imread('android-icon-192x192.png')

# Vérifier si l'image est chargée correctement
if image is None:
    print("Impossible de charger l'image.")
    exit()

# Obtenir les dimensions de l'image
hauteur, largeur, _ = image.shape

# Ouvrir un fichier texte en mode écriture
with open('valeurs_pixels.txt', 'w') as fichier:
    # Parcourir chaque pixel de l'image
    for y in range(hauteur):
        for x in range(largeur):
            pixel = image[y, x]
            # Écrire les valeurs des pixels dans le fichier
            fichier.write(str(pixel) + '\n')

print("Les valeurs des pixels ont été écrites dans 'valeurs_pixels.txt'.")
