import numpy as np
import datagenerator as dg
import tensorflow as tf 
import analyzefit as af
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing


# Car brand and models
brands ={'toyota': ['tacoma', 'tundra', 'camry', 'corolla', 'rav4', '4runner'],
         'subaru': ['outback', 'forester', 'wrx'],
         'honda' : ['civic', 'accord']
        }
categories = ['price', 'year', 'manufacturer', 'model', 'condition', 'odometer'] 
features = [brands, "year", "condition", "mileage"]
labels = ["price"]

data = dg.DataGenerator('vehicles.csv', 'output.csv', categories,  features, labels)

train_features, train_labels = data.load_data()

def hash_input(features):
    # Create list of unique words
    words = []
    for row in features:
        for column in row:
            if type(column) == str:
                if column not in words:
                    words.append(column)
    # Create hash table
    hash_table = {}
    for i, word in enumerate(words):
        hash_table[word] = i
    # Replace where values within features
    for key in hash_table.keys():
        features = np.where(features == key, hash_table[key], features)

    print(hash_table)

    return features
    


train_features = hash_input(train_features)


normalize = preprocessing.Normalization()
normalize.adapt(train_features)

model = tf.keras.Sequential([
    normalize,
    layers.Dense(128, activation="relu"),
    layers.Dense(32, activation="relu"),
    layers.Dense(1)
])

model.compile(loss = tf.losses.MeanSquaredError(), optimizer = tf.optimizers.Adam(.02))

history = model.fit(train_features.astype(float), train_labels.astype(float), batch_size=32, validation_split=0.3, epochs=50, shuffle=True)

# Toyota tacoma
print(model.predict([[2020.0, 0.0, 1.0, 0.0, 10000.0]]))
print(model.predict([[2020.0, 0.0, 1.0, 0.0, 100000.0]]))

graph = af.AnalyzeFit("Fit Data", "Epochs", "Loss")
graph.add_data([history.history['loss'], history.history['val_loss']])
graph.show()