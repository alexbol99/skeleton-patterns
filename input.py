def read_data(filename):
    with open(filename) as file:
        data = file.readlines()
    data = [x.strip() for x in data]
    data = [x.split(' ') for x in data]

    data = [ [float(str) for str in row] for row in data ]
    return data

