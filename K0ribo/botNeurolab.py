import numpy as np
import neurolab as nl
import os
import collections
import datetime

#alle inputs aus der csv
tmp_input_data = []
tmp_input_data_result = []

#70% train data
train_input_data = []
train_input_data_result = []

#30% evaluation data
eval_input_data = []
eval_input_data_result = []

#anpassung der werte
multiplier= 100000

def train_neural_network():
    #von bis
    input0 = [0,1440]
    input1 = [0,multiplier]
    input2 = [0,10000] # ggf anpassen
    #input3 = [0,10000000] # schlecht
    input4 = [-1,2]
    input5 = [-1,5]
    input6 = [-1,10]
    input7 = [0,multiplier] 

    inp_trans = np.array(train_input_data,np.float)
    eval_inp_trans = np.array(eval_input_data, np.float)
    tar_trans = np.array(train_input_data_result,np.float)
    tar_trans = tar_trans.reshape(len(train_input_data_result),1)
    print(inp_trans)
    print("")
    print(tar_trans)


    # 3 hidden layer mit je 6 neuronen
    # outputlayer mit einem output neuron

    net = nl.net.newff([input0,input1,input2,input4,input5,input6],[6,6,5,1])

    #print(net.ci)
    #print(net.co)
    #print(len(net.layers))
    #net.trainf= nl.train.train_gdx

    error = net.train(inp_trans,tar_trans,epochs = 10000,show=100, goal=0.000000001)
    out = net.sim(eval_inp_trans)

    #print(out)
    printIOCompare(eval_input_data_result,out)


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
            for i in range (0,6):
                if i==1:
                    line_data.append(float(row[i])*multiplier)
                else:
                    line_data.append(float(row[i]))

            tmp_input_data_result.append(float(row[6])*multiplier)
            tmp_input_data.append(line_data)

def splitData():
    set_length= len(tmp_input_data)

    train_length = round(set_length * 0.7)

    #trainingsdaten
    for i in range(0,train_length):
        train_input_data.append(tmp_input_data[i])
        train_input_data_result.append(tmp_input_data_result[i])

    #eval
    for j in range(train_length,set_length):
        eval_input_data.append(tmp_input_data[j])
        eval_input_data_result.append(tmp_input_data_result[j])


def main():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = '../Bittrex Extract/brain_out.csv'
    #rel_path = 'test_data.csv'
    abs_file_path = os.path.join(script_dir, rel_path)

    readCSVFile(abs_file_path)

    splitData()

    train_neural_network()

if __name__ == "__main__":
    main()
