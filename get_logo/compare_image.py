import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def load_image(file_path):
    # Charge une image et la convertit en niveau de gris
    image = cv2.imread(file_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def resize_image(image, size):
    # Redimensionne une image à la taille spécifiée
    resized_image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    return resized_image

def compare_images(image1, image2):
    # Compare deux images et retourne un score de similarité entre 0 et 1
    size = (min(image1.shape[1], image2.shape[1]), min(image1.shape[0], image2.shape[0]))
    
    # Redimensionner les images à la même taille
    resized_image1 = resize_image(image1, size)
    resized_image2 = resize_image(image2, size)
    
    # Calcul de la similarité structurelle (SSIM)
    similarity, _ = ssim(resized_image1, resized_image2, full=True)
    
    return similarity

def main():
    # Spécifiez les chemins des deux images à comparer
    image1_path = '1-favicon-32x32.png'
    image2_path = 'favicon-32x32.png'
    
    # Chargez les images
    image1 = load_image(image1_path)
    image2 = load_image(image2_path)
    
    # Comparez les images et obtenez un score de similarité
    similarity_score = compare_images(image1, image2)
    
    print(f"Score de ressemblance entre les images : {similarity_score:.2f}")

if __name__ == '__main__':
    main()
