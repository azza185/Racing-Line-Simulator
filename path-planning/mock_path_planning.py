import numpy as np
import matplotlib

# global_map_mock = []
# global_map_mock2 = []
# global_map_mock3 = []

class Cone:
    x_pos = None
    y_pos = None
    x_differ = None
    y_differ = None
    colour_id = None
    colour = None

    def __init__(self, x_pos, y_pos, colour_id, x_difference = None, y_difference = None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_differ = x_difference
        self.y_differ = y_difference
        if (colour_id in range(0,3)):
            self.colour_id = colour_id
        
        if (self.colour_id != None):
            self.calculate_colour()
    
    def return_colour(self):
        if self.colour:
            return self.colour
        else:
            return "None"
        
    def calculate_colour(self):
        if self.colour_id == 0:
            self.colour = "orange"
        elif self.colour_id == 1:
            self.colour = "blue"
        elif self.colour_id == 2:
            self.colour = "yellow"
    
    def __str__(self) -> str:
        return "Colour: " + self.return_colour() + "\tX-Coord: " + str(self.x_pos) + "\tY-Coord: " + str(self.y_pos)


def generate_data(filepath):
    map_mock = []
    formatted_raw_data = []

    with open(filepath) as f:
        reader = f.read().splitlines()
        test_data_raw = reader[1:]

    for line in test_data_raw:
        split_line = line.split(",")

        for i, num in enumerate(split_line):
            split_line[i] = float(num)


        formatted_raw_data.append(split_line)



    for data in formatted_raw_data:
        map_mock.append(Cone(data[0], data[1], data[2]))

    return map_mock

# def generate_data2(filepath):
#     formatted_raw_data = []

#     with open(filepath) as f:
#         reader = f.read().splitlines()
#         test_data_raw = reader[1:]

#     for line in test_data_raw:
#         split_line = line.split(",")

#         for i, num in enumerate(split_line):
#             split_line[i] = float(num)


#         formatted_raw_data.append(split_line)



#     for data in formatted_raw_data:
#         global_map_mock2.append(Cone(data[0], data[1], data[2]))

# def generate_data3(filepath):
#     formatted_raw_data = []

#     with open(filepath) as f:
#         reader = f.read().splitlines()
#         test_data_raw = reader[1:]

#     for line in test_data_raw:
#         split_line = line.split(",")

#         for i, num in enumerate(split_line):
#             split_line[i] = float(num)


#         formatted_raw_data.append(split_line)



#     for data in formatted_raw_data:
#         global_map_mock3.append(Cone(data[0], data[1], data[2]))
    


mm1 = generate_data('./Test_Data/Path-Planning-Test-Data.csv')
mm2 = generate_data("./Test_Data/Track2.csv")
#mm3 = generate_data('./src/vroomba/Test_Data/third_track.csv')
#mm4 = generate_data("./src/vroomba/Test_Data/fourth_track.csv")

# for cone in mm4:
#     print(cone)



