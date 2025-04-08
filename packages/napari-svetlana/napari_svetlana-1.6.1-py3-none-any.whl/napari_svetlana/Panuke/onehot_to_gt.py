import numpy as np
import os
from skimage.io import imsave


"""
Generation of groundtruth from onehot-encoding to label-encoding for Panuke dataset
"""

# Supposons que vous avez un tableau masks de forme (nombre_images, x, y, 6)
masks = np.load("/home/cazorla/Images/Panuke/Part 1/Masks/masks.npy")

masks_reordered = np.roll(masks, shift=1, axis=-1)

# Calculer le label dominant pour chaque pixel
labels_dominants = np.argmax(masks_reordered, axis=-1)

# Ajuster les valeurs des labels selon votre convention
# (Background vaut 0, Neoplastic cells vaut 1, Inflammatory vaut 2, etc.)
#labels_dominants = np.where(labels_dominants == 3, 0, labels_dominants + 1)

# Afficher les labels dominants pour la première image par exemple
print("Labels dominants pour la première image :\n", labels_dominants[0])
import matplotlib.pyplot as plt

plt.imshow(labels_dominants[0]);
plt.colorbar(

);
plt.show();

for i in range(labels_dominants.shape[0]):
    imsave(os.path.join("/home/cazorla/Images/Panuke/Part 1/training_test/groundtruth", f'gt_{i + 1}.tif'), labels_dominants[i])
