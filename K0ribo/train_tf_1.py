import tensorflow as tf
import os


'''
minutes = tf.feature_column.numeric_column("minutes")
price = tf.feature_column.numeric_column("price")
transactions_amount = tf.feature_column.numeric_column("trans_amount")
coin_amount = tf.feature_column.numeric_column("coin_amount")
past_small = tf.feature_column.numeric_column("change_sm")
past_medium = tf.feature_column.numeric_column("change_md")
past_large = tf.feature_column.numeric_column("change_lg")
'''

CSV_COLUMNS = ["minutes","price","trans_amount","coin_amount","change_sm","change_md","change_lg","t0_price"]

#read csv

n_nodes_hl1= 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 1
batch_size = 100

input_data = []
input_data_result = []

training_data = []
train_data = []

#
x = tf.placeholder('float',[None, 7])

def readCSVFile(file_dir):

    import csv
    with open(file_dir) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        csvfile.readline()
        for row in readCSV:
            line_data = []
            for i in range (0,6):
                line_data.append(row[i])

            input_data_result.append(row[7])
            input_data.append(line_data)

    print(input_data)
    print (input_data_result)

def neural_network_model(data):
    hidden_1_layer = {'weights':tf.Variable(tf.random_normal([7,n_nodes_hl1])),
                        'biases':tf.Variable(tf.random_normal(n_nodes_hl1))}

    hidden_2_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1,n_nodes_hl2])),
                        'biases':tf.Variable(tf.random_normal(n_nodes_hl2))}

    hidden_3_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2,n_nodes_hl3])),
                        'biases':tf.Variable(tf.random_normal(n_nodes_hl3))}

    hidden_output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl3,n_classes])),
                        'biases':tf.Variable(tf.random_normal(n_classes))}       


    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights'])+hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)

    l2= tf.add(tf.matmul(l1, hidden_2_layer['weights'])+hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights'])+hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, hidden_output_layer['weights'])+hidden_output_layer['biases']
    
    return output

def main():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = 'test_data.csv'
    abs_file_path = os.path.join(script_dir, rel_path)

    readCSVFile(abs_file_path)

if __name__ == "__main__":
    main()

