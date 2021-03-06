# def read_data(filename):
#     with open(filename) as file:
#         data = file.readlines()
#     file.close()
#     data = [x.strip() for x in data]
#     data = [x.split(',') for x in data]
#
#     data = [ [float(str) for str in row] for row in data ]
#     return data

import csv

def read_data(filename):
    with open(filename, 'r') as f:
      reader = csv.reader(f)
      data = [[float(str) for str in row] for row in list(reader)]
    return data

