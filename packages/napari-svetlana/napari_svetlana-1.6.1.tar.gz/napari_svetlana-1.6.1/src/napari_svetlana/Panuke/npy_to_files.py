import numpy as np
from skimage.io import imsave
import os

"""
This script converts the npy file of the Panuke dataset containing the images to tif single RGB images.
"""

# Charger le fichier npy
folder = "/home/cazorla/Images/Panuke/Part 1/Images"
data = np.load(os.path.join(folder, "images.npy"))

# Boucle pour enregistrer chaque image en tant que fichier TIFF
for i in range(data.shape[0]):
    # Extrait l'image RGB
    image_rgb = data[i]
    # Enregistre l'image en tant que fichier TIFF
    imsave(os.path.join(folder, f'image_{i + 1}.tif'), image_rgb.astype("uint16"))

print("Les images ont été enregistrées avec succès.")
