import numpy as np
from sklearn.metrics import accuracy_score, f1_score, recall_score, balanced_accuracy_score, precision_recall_fscore_support
from skimage.io import imread
import os
from natsort import natsorted

folder = "/home/cazorla/Images/Panuke/Part 1/train_test_100"

pred_folder = os.path.join(folder, "Predictions")
gt_folder = os.path.join(folder, "groundtruth")

pred_path = natsorted(os.listdir(pred_folder))
gt_path = []
for p in pred_path:
    gt_path.append(os.path.join(gt_folder, "gt_" + p.split("_")[-1]))

n = len(pred_path)

images = [imread(os.path.join(pred_folder, pred_path[i])) for i in range(n)]  # Exemple de tableau 2D pour chaque image
verites_terrain = [imread(os.path.join(gt_folder, gt_path[i])) for i in range(n)]  # Exemple de tableau 2D pour chaque vérité de terrain

# Initialiser des listes pour stocker les résultats
accuracies = []
balanced_accuracies = []
f1_scores = []
recalls = []

# Calculer les métriques pour chaque image
for i in range(0, n):
    vraies_etiquettes_flatten = verites_terrain[i].flatten()
    predictions_flatten = images[i].flatten()

    """
    # Calcul de l'accuracy pour chaque image
    accuracy = accuracy_score(vraies_etiquettes_flatten, predictions_flatten)
    accuracies.append(accuracy)

    # Calcul de l'accuracy équilibrée pour chaque image
    balanced_accuracy = balanced_accuracy_score(vraies_etiquettes_flatten, predictions_flatten)
    balanced_accuracies.append(balanced_accuracy)

    # Calcul du F1-score pour chaque image
    f1 = f1_score(vraies_etiquettes_flatten, predictions_flatten, average='weighted')  # 'weighted' pour la moyenne pondérée
    f1_scores.append(f1)

    # Calcul du rappel pour chaque image
    recall = recall_score(vraies_etiquettes_flatten, predictions_flatten, average='weighted')  # 'weighted' pour la moyenne pondérée
    recalls.append(recall)"""
    precision, recall, F1, _ = precision_recall_fscore_support(vraies_etiquettes_flatten, predictions_flatten, average='weighted')
    accuracies.append(precision)
    f1_scores.append(F1)
    recalls.append(recall)

# Calculer la moyenne des métriques sur l'ensemble du dataset
accuracy_moyenne = np.mean(accuracies)
#balanced_accuracy_moyenne = np.mean(balanced_accuracies)
f1_moyen = np.mean(f1_scores)
recall_moyen = np.mean(recalls)

print(f'Accuracy moyenne sur l\'ensemble du dataset : {accuracy_moyenne}')
#print(f'Balanced accuracy moyenne sur l\'ensemble du dataset : {balanced_accuracy_moyenne}')
print(f'F1-Score moyen sur l\'ensemble du dataset : {f1_moyen}')
print(f'Rappel moyen sur l\'ensemble du dataset : {recall_moyen}')
