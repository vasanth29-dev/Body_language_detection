import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

X = np.random.rand(200,48,48,1)
y = tf.keras.utils.to_categorical(np.random.randint(0,7,200), 7)

model = models.Sequential()

model.add(layers.Conv2D(32,(3,3),activation='relu',input_shape=(48,48,1)))
model.add(layers.MaxPooling2D(2,2))

model.add(layers.Conv2D(64,(3,3),activation='relu'))
model.add(layers.MaxPooling2D(2,2))

model.add(layers.Conv2D(128,(3,3),activation='relu'))
model.add(layers.MaxPooling2D(2,2))

model.add(layers.Flatten())
model.add(layers.Dense(128,activation='relu'))
model.add(layers.Dropout(0.5))

model.add(layers.Dense(7,activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X,y,epochs=5)

model.save("emotion_model.keras")

print("Model trained successfully!")