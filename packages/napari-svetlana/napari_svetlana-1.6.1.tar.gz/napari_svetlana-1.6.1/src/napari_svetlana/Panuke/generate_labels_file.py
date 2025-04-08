import numpy as np
from skimage.io import imread
import os
from natsort import natsorted
from skimage.measure import regionprops
import torch

"""
Generate the Svetlana-compliant labels file from the Panuke dataset labels
"""

images_folder = "/home/cazorla/Images/Panuke/Part 1/training_frugal/Images"
masks_folder = "/home/cazorla/Images/Panuke/Part 1/training_frugal/Masks"
mask_npy_path = os.path.join("/home/cazorla/Images/Panuke/Part 1/Masks", "masks.npy")

masks_npy = np.load(mask_npy_path)

image_path = []
# Parcourir les fichiers du dossier
for fichier in natsorted(os.listdir(images_folder)):
    # Vérifier si le fichier est un fichier TIFF
    if fichier.endswith('.tif') or fichier.endswith('.tiff'):
        # Construire le chemin complet du fichier
        chemin_complet = os.path.join(images_folder, fichier)
        # Ajouter le chemin à la liste
        image_path.append(chemin_complet)

labels_path = []
# Parcourir les fichiers du dossier
for fichier in natsorted(os.listdir(masks_folder)):
    # Vérifier si le fichier est un fichier TIFF
    if fichier.endswith('.tif') or fichier.endswith('.tiff'):
        # Construire le chemin complet du fichier
        chemin_complet = os.path.join(masks_folder, fichier)
        # Ajouter le chemin à la liste
        labels_path.append(chemin_complet)

props_list = []
labels_list = []

# liste des régionprops pour chaque image
for i, m_name in enumerate(labels_path):
    l_props = []
    l_labs = []
    mask = imread(m_name)
    rprops = regionprops(mask)
    index = int(os.path.split(m_name)[1].split("_")[1].split(".")[0]) - 1
    for p in rprops:
        l_props.append({"centroid": p.centroid, "coords": p.coords, "label": p.label})
        l_labs.append(np.argmax(masks_npy[index][int(p.centroid[0]), int(p.centroid[1])], axis=-1))
    props_list.append(l_props)
    labels_list.append(l_labs)

# Regionprops over all the masks so the size si computed using the biggest object of the whole dataset
props = []
for p in labels_path:
    labels = imread(p)
    props += regionprops(labels)

x = sorted(props, key=lambda r: r.area, reverse=True)

# Cas 2D/3D
if len(labels.shape) == 2:
    xmax = x[0].bbox[2] - x[0].bbox[0]
    ymax = x[0].bbox[3] - x[0].bbox[1]
    length = max(xmax, ymax)
else:
    xmax = x[0].bbox[3] - x[0].bbox[0]
    ymax = x[0].bbox[4] - x[0].bbox[1]
    zmax = x[0].bbox[5] - x[0].bbox[2]
    length = max(xmax, ymax, zmax)

patch_size = int(length + 0.4 * length)

labels_dict = {"image_path": image_path, "labels_path": labels_path, "regionprops": props_list,
               "labels_list": labels_list, "patch_size": patch_size}

torch.save(labels_dict, "/home/cazorla/Images/Panuke/Part 1/training_frugal/Svetlana/labels")
