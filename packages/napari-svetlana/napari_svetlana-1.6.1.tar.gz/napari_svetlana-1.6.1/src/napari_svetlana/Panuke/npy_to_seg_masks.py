import numpy as np
from PIL import Image
import os
from skimage.measure import label

"""
Generate tif mask files from the npy fil of Panuke dataset
"""

folder = "/home/cazorla/Images/Panuke/Part 1/Masks"
# Charger le fichier npy
data = np.load(os.path.join(folder, "masks.npy"))


# Boucle pour enregistrer chaque masque en tant que fichier TIFF
for i in range(data.shape[0]):
    # Créer un masque à partir des canaux (ignorez le canal Background)
    mask = np.sum(data[i, :, :, :5], axis=-1)

    # Convertir le masque en objet Image
    mask_image = Image.fromarray(label(mask).astype(np.uint16))

    # Enregistrer le masque en tant que fichier TIFF
    mask_image.save(os.path.join(folder, f'mask_{i + 1}.tif'))

print("Les masques ont été générés et enregistrés avec succès.")

