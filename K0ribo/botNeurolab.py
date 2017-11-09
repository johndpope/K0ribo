import numpy as np
import neurolab as nl
import os
import collections
import datetime

input_data = []
input_data_result = []

def train_neural_network():
    #von bis
    input0 = [0,1440]
    input1 = [0,1]
    input2 = [0,10000] # ggf anpassen
    #input3 = [0,10000000] # schlecht
    input4 = [-2,2]
    input5 = [-5,5]
    input6 = [-10,10]
    input7 = [0,1] 

    inp_trans = np.array(input_data,np.float)
    tar_trans = np.array(input_data_result,np.float)
    tar_trans = tar_trans.reshape(len(input_data_result),1)
    print(inp_trans)
    print("")
    print(tar_trans)


    # 3 hidden layer mit je 6 neuronen
    # outputlayer mit einem output neuron

    net = nl.net.newff([input0,input1,input2,input4,input5,input6],[6,6,1])

    #print(net.ci)
    #print(net.co)
    #print(len(net.layers))
    net.trainf= nl.train.train_gdx

    error = net.train(inp_trans,tar_trans,epochs = 9000,show=100, goal=0.000001)
    out = net.sim(inp_trans)

    #print(out)
    printIOCompare(input_data_result,out)


def printIOCompare(exp,outp):
    lenght = len(outp)
    for i in range(0,lenght):
        print("Expected: ",exp[i], "\tResult: ",outp[i])    


def readCSVFile(file_dir):

    import csv
    with open(file_dir) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        for row in readCSV:
            line_data = []
            for i in range (0,7):
                line_data.append(float(row[i]))

            input_data_result.append(float(row[7]))
            input_data.append(line_data)

def main():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = '../Bittrex Extract/brain_out.csv'
    #rel_path = 'test_data.csv'
    abs_file_path = os.path.join(script_dir, rel_path)

    readCSVFile(abs_file_path)

    train_neural_network()

if __name__ == "__main__":
    main()
