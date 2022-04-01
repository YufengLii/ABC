# https://www.freecodecamp.org/news/how-to-build-and-train-k-nearest-neighbors-ml-models-in-python/

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

raw_data = pd.read_csv('../dataset/old_dataset.csv')
# print(raw_data.columns)

scaler = StandardScaler()
scaler.fit(raw_data.drop('TARGET_CLASS', axis=1))
scaled_features = scaler.transform(raw_data.drop('TARGET_CLASS', axis=1))
scaled_data = pd.DataFrame(scaled_features, columns=raw_data.drop('TARGET_CLASS', axis=1).columns)

x = scaled_data
y = raw_data['TARGET_CLASS']

x_training_data, x_test_data, y_training_data, y_test_data = train_test_split(x, y, test_size=0.3)

model = KNeighborsClassifier(n_neighbors=1)
model.fit(x_training_data, y_training_data)

predictions = model.predict(x_test_data)

# print(classification_report(y_test_data, predictions))
# print(confusion_matrix(y_test_data, predictions))

error_rates = []

for i in np.arange(1, 101):
    new_model = KNeighborsClassifier(n_neighbors=i)
    new_model.fit(x_training_data, y_training_data)
    new_predictions = new_model.predict(x_test_data)
    error_rates.append(np.mean(new_predictions != y_test_data))

plt.plot(error_rates)
plt.show()
