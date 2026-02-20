import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import tensorflow as tf
from tensorflow import keras
from NN_test.utils import rname, remake, convert, get_base_dir


# test_photo = f"./train_npy/2/2_31.npy"
# test_photo_ex = f"./train_npy/2/2_7.npy"

# array = np.load(test_photo)
# array_ex = np.load(test_photo_ex)

# if len(array.shape) == 2:
#     array = np.expand_dims(array, axis=-1)
#     array = np.expand_dims(array, axis = 0)

# array_ex = np.expand_dims(array_ex, axis=-1)
# array_ex = np.expand_dims(array_ex, axis=0)

# print(array.shape)
# model = tf.keras.models.load_model("./vector_model.keras")

# output_data = model.predict(array)
# out = model.predict(array_ex)

# print(f">>>>>>>> \n {output_data} \n !!!!!!!!!!!!!!!>>....>>>>>>>>>>>>>>>>>>> \n {out}")

# print(f">>>>>>>>")

model = tf.keras.models.load_model("./vector_model.keras")


# def test_func(file_name):
#     test_photo_ex = f"./NN_test/train_npy/2/2_7.npy"

#     Utils.rname(test_photo_ex)

#     Utils.rname(file_name)
#     Utils.convert(file_name)

#     array = np.load(f"./NN_test/test_data/{file_name}.npy")
#     array_ex = np.load(test_photo_ex)

#     if len(array.shape) == 2:
#         array = np.expand_dims(array, axis=-1)
#         array = np.expand_dims(array, axis = 0)

#     array_ex = np.expand_dims(array_ex, axis=-1)
#     array_ex = np.expand_dims(array_ex, axis=0)

#     output_data = model.predict(array)
#     out = model.predict(array_ex)

#     similarity = cosine_similarity(output_data, out)[0][0]

#     return similarity

# NN_test/test.py  (фрагмент)

import os

def test_func(file_name):  # file_name приходит как "test_image"
    base_dir = os.path.dirname(os.path.abspath(__file__))

    ref_npy = os.path.join(base_dir, "train_npy", "34", "34_34.npy")
    test_npy = os.path.join(base_dir, "test_data", f"{file_name}.npy")

    rname(file_name)
    convert(file_name)

    array = np.load(test_npy)
    array_ex = np.load(ref_npy)

    array = np.expand_dims(array, -1)         
    array = np.expand_dims(array,  0)                               

    array_ex = np.expand_dims(array_ex, axis=-1)
    array_ex = np.expand_dims(array_ex, axis=0)

    output_data = model.predict(array, verbose=0)
    out = model.predict(array_ex, verbose=0)

    similarity = cosine_similarity(output_data, out)[0][0]

    similarity = float(similarity) 

    return similarity

# similarity = cosine_similarity(output_data, out)[0][0]
# distance = 1 - similarity 

# print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {similarity} {distance}")

# model = tf.keras.models.load_model("./embedding_model_trained.keras")
# ress = []

# for i in range(1,40):
#     for j in range(1,40):

#         test_photo = f"./train_npy/{i}/{i}_{i}.npy"
#         test_photo_ex = f"./train_npy/{i}/{i}_{j}.npy"

#         array = np.load(test_photo)
#         array_ex = np.load(test_photo_ex)

#         if len(array.shape) == 2:
#             array = np.expand_dims(array, axis=-1)
#             array = np.expand_dims(array, axis = 0)

#         array_ex = np.expand_dims(array_ex, axis=-1)
#         array_ex = np.expand_dims(array_ex, axis=0)


#         output_data = model.predict(array)
#         out = model.predict(array_ex)

#         bins = np.linspace(-0.2, 1.0, 41) 
#         alpha = 0.7
#         figsize = (10, 6)

#         res = tf.reduce_sum(out * output_data, axis=1).numpy().item()

#         ress.append(res)

# plt.figure(figsize=figsize)
# plt.hist(ress, bins=bins, alpha=alpha, color='green', label='Positive (same person)',
#         density=True, edgecolor='black', linewidth=0.5)
# # plt.hist(neg_sim, bins=bins, alpha=alpha, color='red', label='Negative (different persons)',
# #         density=True, edgecolor='black', linewidth=0.5)
# plt.axvline(np.mean(ress), color='darkgreen', linestyle='--', linewidth=2,
#             label=f'Positive mean = {np.mean(ress):.3f}')
# # plt.axvline(np.mean(neg_sim), color='darkred', linestyle='--', linewidth=2,
# #             label=f'Negative mean = {np.mean(neg_sim):.3f}')
# plt.grid(True, alpha=0.3, linestyle='--')
# plt.savefig('bbbb.png', dpi=150, bbox_inches='tight')
# plt.show()
