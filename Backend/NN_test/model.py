# import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from keras.layers import Flatten, Dense
# from data import Data


# def emb_model(image_input = tf.keras.Input(shape = (192,168,1)), embedding_dim = 128):
#     x = keras.layers.Conv2D(32, kernel_size=3, padding='same')(image_input)
#     x = keras.layers.BatchNormalization()(x)
#     x = keras.layers.ReLU()(x)
#     x = keras.layers.MaxPooling2D(pool_size=2)(x)
#     x = keras.layers.Conv2D(64, kernel_size=3, padding='same')(x)
#     x = keras.layers.BatchNormalization()(x)
#     x = keras.layers.ReLU()(x)
#     x = keras.layers.MaxPooling2D(pool_size=2)(x)   
#     x = keras.layers.Conv2D(128, kernel_size=3, padding='same')(x)
#     x = keras.layers.BatchNormalization()(x)
#     x = keras.layers.ReLU()(x)
#     x = keras.layers.MaxPooling2D(pool_size=2)(x) 
#     x = keras.layers.Conv2D(192, kernel_size=3, padding='same')(x)
#     x = keras.layers.BatchNormalization()(x)
#     x = keras.layers.ReLU()(x)
#     x = keras.layers.MaxPooling2D(pool_size=2)(x)     
#     x = keras.layers.Conv2D(168, kernel_size=3, padding='same')(x)
#     x = keras.layers.BatchNormalization()(x)
#     x = keras.layers.ReLU()(x)
#     x = keras.layers.GlobalAveragePooling2D()(x) 
#     x = keras.layers.Dense(256, activation='relu')(x)
#     x = keras.layers.Dropout(0.1)(x)
#     x = keras.layers.Dense(128, activation='relu')(x)

#     embeddings = keras.layers.Dense(embedding_dim, name='embeddings')(x)
#     model = keras.Model(inputs=image_input, outputs=embeddings, name='embedding_model')
#     return model


# def triplet_loss_direct(y_pred, margin=0.2):
#     anchor = y_pred[:, 0, :, :, :]
#     positive = y_pred[:, 1, :, :, :]
#     negative = y_pred[:, 2, :, :, :]        
    
#     anchor_emb = emodel(anchor)      
#     positive_emb = emodel(positive)    
#     negative_emb = emodel(negative)
    
#     pos_dist = tf.reduce_sum(tf.square(anchor_emb - positive_emb), axis=1)
#     neg_dist = tf.reduce_sum(tf.square(anchor_emb - negative_emb), axis=1)
    
#     basic_loss = pos_dist - neg_dist + margin
#     return tf.reduce_mean(tf.maximum(basic_loss, 0.0))
        

# def compile_model():
#     inputs = keras.Input(shape=(192, 168, 1))
#     model = emb_model(inputs)
        
#     model.compile(optimizer='adam')
#     return model


# def train(model):
#     epochs = 2

#     for epoch in range(epochs):
#         for step, (x_batch_train, y_batch_train) in enumerate(train_dataset):
#             with tf.GradientTape() as tape:
#                 logits = model(x_batch_train, training=True)

#                 loss_value = loss_fn(y_batch_train, logits)

#             grads = tape.gradient(loss_value, model.trainable_weights)
#             optimizer.apply_gradients(zip(grads, model.trainable_weights))


# if __name__ == "__main__":
#     compile_model()
#     # X_train = len(Data().get_data_for_training())
#     # y_train = np.zeros(X_train)

#     # model.fit(Data().get_data_for_training(), y_train,
#     #             epochs=10,
#     #             shuffle=True,
#     #             validation_data=(Data().get_data_for_training(), y_train))
  
#     # model.save("./test_model.h5")


import numpy as np
import tensorflow as tf
from keras import layers, Model, regularizers
from data import Data  


def build_embedding_model(input_shape = (192, 168, 1), embedding_dim=512):
    inputs = layers.Input(shape=input_shape)
    
    x = layers.Conv2D(32, 3, padding='same', kernel_regularizer=regularizers.l2(1e-5))(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(2)(x)
    
    x = layers.Conv2D(64, 3, padding='same', kernel_regularizer=regularizers.l2(1e-5))(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(2)(x)
    
    x = layers.Conv2D(128, 3, padding='same', kernel_regularizer=regularizers.l2(1e-5))(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(2)(x)
    
    x = layers.Conv2D(256, 3, padding='same', kernel_regularizer=regularizers.l2(1e-5))(x)   
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.MaxPooling2D(2)(x)
    
    x = layers.Conv2D(192, 3, padding='same', kernel_regularizer=regularizers.l2(1e-5))(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    
    x = layers.GlobalAveragePooling2D()(x)
    
    x = layers.Dense(512, activation='relu',
                     kernel_regularizer=regularizers.l2(1e-4))(x)
    x = layers.Dropout(0.35)(x)                   
    
    x = layers.Dense(512, activation='relu',
                     kernel_regularizer=regularizers.l2(1e-4))(x)
    x = layers.Dropout(0.25)(x)
    
    embeddings = layers.Dense(embedding_dim,
                              kernel_regularizer=regularizers.l2(1e-4))(x)
    
    embeddings = layers.UnitNormalization(axis=1)(embeddings)
    
    return Model(inputs, embeddings, name='embedding_model')

def triplet_loss_cosine(anchor_emb, positive_emb, negative_emb, margin=0.2):
    pos_cos = tf.reduce_sum(anchor_emb * positive_emb, axis=1)
    neg_cos = tf.reduce_sum(anchor_emb * negative_emb, axis=1)

    basic_loss = margin - (pos_cos - neg_cos)
    return tf.reduce_mean(tf.maximum(basic_loss, 0.0))



if __name__ == "__main__":

    triplets = Data().get_data_for_training()
    
    N = triplets.shape[0]
    
    BATCH_SIZE = 64
    EPOCHS = 10
    steps_per_epoch = (N + BATCH_SIZE - 1) // BATCH_SIZE 
    
    model = build_embedding_model()
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0003)
    
    for epoch in range(EPOCHS):
        print(f"EPOCH {epoch+1}/{EPOCHS}")
        
        total_loss = 0.0
        num_batches = 0
        
        indices = np.random.permutation(N)
        
        for i in range(0, N, BATCH_SIZE):
            batch_indices = indices[i:i + BATCH_SIZE]
            
            batch_triplets = triplets[batch_indices]
            
            anchors   = batch_triplets[:, 0] 
            positives = batch_triplets[:, 1]
            negatives = batch_triplets[:, 2]
             
            with tf.GradientTape() as tape:

                emb_a = model(anchors,   training=True)
                emb_p = model(positives, training=True)
                emb_n = model(negatives, training=True)
                
                loss_value = triplet_loss_cosine(emb_a, emb_p, emb_n)
            
                grads = tape.gradient(loss_value, model.trainable_variables)
        
            optimizer.apply_gradients(zip(grads, model.trainable_variables))
            
            total_loss += float(loss_value) * len(batch_indices)  
            num_batches += len(batch_indices)
            
            step = i // BATCH_SIZE
            if step % 5 == 0 or step == steps_per_epoch - 1:
                print(f"  STEP {step:3d}/{steps_per_epoch} >>>>>>> "
                      f"loss: {loss_value:.4f}")
        
        avg_loss = total_loss / num_batches if num_batches > 0 else 0
        print(f"  loss of epoch: {avg_loss:.4f}")
    
    model.save("vector_model.keras")

    print("model was saved")

