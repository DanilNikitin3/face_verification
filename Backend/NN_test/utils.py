# from PIL import Image
# import numpy as np
# import os
# import math

# class Utils:
#     def __init__(self):
#         pass


#     def delete(self):
        
#         for i in range(2,40):
#             for j in range(51,64):
#                 if i != 14:
#                     os.remove(f'./train_data/{i}/{i}_{j}.jpg')

#         for i in range(12,40):
#             if i != 14:
#                 if math.floor(i / 9) == 0:
#                     os.remove(f'./CroppedYale/yaleB0{i}/yaleB0{i}_P00_Ambient.pgm')
#                     os.remove((f'./CroppedYale/yaleB0{i}/WS_FTP.LOG'))
#                     os.remove((f'./CroppedYale/yaleB0{i}/yaleB0{i}_P00.info'))
#                 else:
#                     os.remove(f'./CroppedYale/yaleB{i}/yaleB{i}_P00_Ambient.pgm')
#                     os.remove((f'./CroppedYale/yaleB{i}/WS_FTP.LOG'))
#                     os.remove((f'./CroppedYale/yaleB{i}/yaleB{i}_P00.info'))


#     def rname(self, file):
#         img = Image.open(f"~/Documents/expo/Backend/NN_test/{file}.jpg")
        
#         img.convert('RGB').save(f'./test_data/{file}.jpg')


#     def rename(self,number, file):
#         count = 0

#         # for i in range(1,40):
#         #     os.makedirs(f"./train_data/{i}")

#         for filename in os.listdir(file):

#             img = Image.open(f"{file}/{filename}")
            
#             img.convert('RGB').save(f'./train_data/{number}/{number}_{count}.jpg')
#             count += 1


#     def remake(self, file):
#         image = Image.open(f'./test_data/{file}.jpg').convert('L') 
#         matrix = np.array(image, dtype=float)

#         for j in range(len(matrix)):
#             for i in range(len(matrix[0])):

#                 matrix[j][i] = (matrix[j][i] / 255)
        
#         return matrix


#     def convert(self, file):

#         # for i in range(51):
#             # image = Image.open(f'./train_data/{number}/{number}_{i}.jpeg').convert('L') 
#             # matrix = np.array(image)

#             np.save(f'./test_data/{file}.npy', self.remake(file))


# if __name__ == "__main__":
    
#     Utils().delete()

#     for i in range(1,40):
#         if i != 14:
#             if math.floor(i / 10) == 0:
#                 Utils().rename(i,f'./CroppedYale/yaleB0{i}/')
#             else:
#                 Utils().rename(i,f'./CroppedYale/yaleB{i}/')

#     for i in range(1,40):
#         if i != 14:
#             Utils().convert(i)



from PIL import Image
import numpy as np
import os

def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def rname(file_name):
    base_dir = get_base_dir()

    input_path = os.path.join(base_dir, file_name)     
    input_path = f"{input_path}.jpg"
    output_path = os.path.join(base_dir, "test_data", f"{file_name}.jpg")

    img = Image.open(input_path)
    img = img.convert('RGB')
    img.save(output_path)


def remake(jpg_path):
    image = Image.open(jpg_path).convert('L')
    matrix = np.array(image, dtype=np.float32)
    matrix /= 255.0
    return matrix


def convert(file_name):
    base_dir = get_base_dir()
    jpg_path = os.path.join(base_dir, "test_data", f"{file_name}.jpg")
    npy_path = os.path.join(base_dir, "test_data", f"{file_name}.npy")

    matrix = remake(jpg_path)
    np.save(npy_path, matrix)

