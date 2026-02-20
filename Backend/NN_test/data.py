import numpy as np
import random
import glob
from math import floor
import os
import tensorflow as tf


class Data:
    def __init__(self):
        self.const = 1989
        self.train_const = 3


    def file_choice(self, array):
        self.array = array
        self.file = random.choice(self.array)

        return self.file
    

    def get_test_sample(self):
        self.npy_files = glob.glob('./train_data/*.npy')
    
        self.random_file = random.choice(self.npy_files)
        self.array = np.load(self.random_file)
        
        return self.array


    def rand(self, number, count):
        self.number = number

        self.using = [item for item in range(1, count) if item != self.number]
        self.final = self.file_choice(self.using)

        return self.final


    def get_data_for_training(self):
        
        X_train = []
        count = 0 
                
        for file_num in range(self.const):
            main_array = []

            random_number = self.rand(floor(count / 51), 39)

            file_paths = [f'./train_npy/{(floor(file_num / 51)) + 1}/{(floor(file_num / 51)) + 1}_{(file_num % 51)}.npy',
                            f'./train_npy/{(floor(file_num / 51)) + 1}/{(floor(file_num / 51)) + 1}_{self.rand(file_num % 51, 50)}.npy',
                            f'./train_npy/{random_number + 1}/{random_number + 1}_{count % 51}.npy']

            for dt in file_paths:
                array = np.load(dt)
                if len(array.shape) == 2:
                    array = np.expand_dims(array, axis=-1)
                main_array.append(array)
                    
            X_train.append(main_array)
            count += 1
    
        return np.array(X_train)


    # def embeded():

    #   Y_train = []

    #   for data in Data().get_data_for_training():
    #       train = []

    #       for dt in data:
    #           array = dt

    #       Y_train.append(train)

    #   return np.load(Y_train)


if __name__ == "__main__":
    data = Data()

    X_train = data.get_data_for_training()
    
    print(f"train >>>>>>>>>>>>> {X_train.shape}")

    test_array = Data.get_test_sample
    print(f" array >>>>>>>>> {test_array}")


