import os
import random
import torch
import shutil

"""
This code generates a sub dataset containing around a given number of labels (e.g. 100) and only two 
labels randomly (e.g. 0 and 2). This dataset aims to evaluate Svetlana's ability to predict accurately 
being trained on a tiny dataset.
"""

# Votre dictionnaire existant
votre_dictionnaire = torch.load("/home/cazorla/Images/Panuke/Part 1/training_test_huge/Svetlana/labels")


# Nombre total de labels que vous voulez dans le nouveau dictionnaire
nombre_total_labels_voulu = 10

# Creation du dossier de destination
dest_path = os.path.join("/home/cazorla/Images/Panuke/Part 1", "train_test_" + str(nombre_total_labels_voulu))
if os.path.exists(dest_path) is False:
    os.mkdir(dest_path)
if os.path.exists(os.path.join(dest_path, "Images")) is False:
    os.mkdir(os.path.join(dest_path, "Images"))
if os.path.exists(os.path.join(dest_path, "Masks")) is False:
    os.mkdir(os.path.join(dest_path, "Masks"))
if os.path.exists(os.path.join(dest_path, "Svetlana")) is False:
    os.mkdir(os.path.join(dest_path, "Svetlana"))

# Labels spécifiques que vous voulez conserver
labels_specifiques = {0, 2}

# Liste pour stocker les images filtrées
images_filtrees = []

# Somme initiale des labels
somme_labels = 0

# Parcourez la liste des labels
for i in range(len(votre_dictionnaire['labels_list'])):
    # Obtenez les labels de l'image actuelle
    labels_image = set(votre_dictionnaire['labels_list'][i])

    # Vérifiez si la liste contient exclusivement les labels spécifiques
    if labels_image.issubset(labels_specifiques):
        # Ajoutez l'image filtrée à la liste
        images_filtrees.append({
            'labels_list': votre_dictionnaire['labels_list'][i],
            'image_path': votre_dictionnaire['image_path'][i],
            'labels_path': votre_dictionnaire['labels_path'][i],
            'regionprops': votre_dictionnaire['regionprops'][i]
        })

        # Mettez à jour la somme des labels
        somme_labels += len(votre_dictionnaire['labels_list'][i])

        # Si la somme atteint ou dépasse la cible, arrêtez la boucle
        if somme_labels >= nombre_total_labels_voulu:
            break

# Nouveau dictionnaire avec les informations des images filtrées
nouveau_dictionnaire = {
    'labels_list': [image['labels_list'] for image in images_filtrees],
    'image_path': [image['image_path'] for image in images_filtrees],
    'labels_path': [image['labels_path'] for image in images_filtrees],
    'regionprops': [image['regionprops'] for image in images_filtrees],
    "patch_size": votre_dictionnaire["patch_size"]
    # ... autres clés ...
}

for i in range(len(nouveau_dictionnaire['image_path'])):
    # Copie des images nécessaires à l'entrainement dans un nouveau dossier
    shutil.copy(nouveau_dictionnaire["image_path"][i], os.path.join(dest_path, "Images", os.path.split(nouveau_dictionnaire["image_path"][i])[1]))
    shutil.copy(nouveau_dictionnaire["labels_path"][i], os.path.join(dest_path, "Masks", os.path.split(nouveau_dictionnaire["labels_path"][i])[1]))
    shutil.copy(os.path.join("/home/cazorla/Images/Panuke/Part 1/training_test_huge/Svetlana/", "Config.json"),
                os.path.join(dest_path, "Svetlana", "Config.json"))
    nouveau_dictionnaire["image_path"][i] = os.path.join(dest_path, "Images", os.path.split(nouveau_dictionnaire["image_path"][i])[1])
    nouveau_dictionnaire["labels_path"][i] = os.path.join(dest_path, "Masks", os.path.split(nouveau_dictionnaire["labels_path"][i])[1])
torch.save(nouveau_dictionnaire, os.path.join(dest_path, "Svetlana", "labels"))
print("Labels créés")