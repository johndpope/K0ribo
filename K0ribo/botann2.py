import tensorflow as tf
import numpy as np
import os
import collections

input_data = []
input_data_result = []





def readCSVFile(file_dir):

    import csv
    with open(file_dir) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        #csvfile.readline()
        for row in readCSV:
            line_data = []
            for i in range (0,7):
                line_data.append(float(row[i]))

            input_data_result.append(float(row[7]))
            input_data.append(line_data)

    #print(input_data)
    #print (input_data_result)

def main():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = '../Bittrex Extract/brain_out.csv'
    #rel_path = 'test_data.csv'
    abs_file_path = os.path.join(script_dir, rel_path)

    readCSVFile(abs_file_path)

    #train_neural_network(x)

if __name__ == "__main__":
    main()