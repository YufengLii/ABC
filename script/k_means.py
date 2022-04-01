# https://www.freecodecamp.org/news/how-to-build-and-train-k-nearest-neighbors-ml-models-in-python/

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

raw_data = make_blobs(n_samples=5000, n_features=2, centers=5, cluster_std=1.8)
# print(raw_data)

_class = []
_x = []
_y = []
count = 0
for line in raw_data:
    if count != 0:
        for number in line:
            _class.append(number)
    else:
        for number in line:
            _x.append(number[0])
            _y.append(number[1])
    count = count + 1

data = []
for i in range(len(_class) - 1):
    data.append([_x[i], _y[i]])  # , _class[i]])

df = pd.DataFrame(data)
df.to_csv('../dataset/old_dataset.csv', index=False)
print(df)

# plt.scatter(raw_data[0][:, 0], raw_data[0][:, 1], c=raw_data[1])
# plt.show()

model = KMeans(n_clusters=5)
model.fit(raw_data[0])
# print(model.labels_)
# print(model.cluster_centers_)

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 6))
ax1.set_title('our model')
ax1.scatter(raw_data[0][:, 0], raw_data[0][:, 1], c=model.labels_)
ax2.set_title('original data')
ax2.scatter(raw_data[0][:, 0], raw_data[0][:, 1], c=raw_data[1])
plt.show()
