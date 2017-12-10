import tensorflow as tf
import os
import collections


'''
minutes = tf.feature_column.numeric_column("minutes")
price = tf.feature_column.numeric_column("price")
transactions_amount = tf.feature_column.numeric_column("trans_amount")
coin_amount = tf.feature_column.numeric_column("coin_amount")
past_small = tf.feature_column.numeric_column("change_sm")
past_medium = tf.feature_column.numeric_column("change_md")
past_large = tf.feature_column.numeric_column("change_lg")
'''

time = tf.feature_column.numeric_column("time")

CSV_COLUMNS = ["minutes","price","trans_amount","coin_amount","change_sm","change_md","change_lg","t0_price"]

#read csv

n_nodes_hl1= 50
n_nodes_hl2 = 50
n_nodes_hl3 = 50

n_classes = 1
batch_size = 100

batch_counter = 0

input_data = []
input_data_result = []


#
x = tf.placeholder('float',[None,7])
y = tf.placeholder('float')

def readCSVFile(file_dir):

    import csv
    with open(file_dir) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        csvfile.readline()
        for row in readCSV:
            line_data = []
            for i in range (0,14):
                line_data.append(float(row[i]))

            input_data_result.append(float(row[14]))
            input_data.append(line_data)

    print(input_data)
    print (input_data_result)

def neural_network_model(data):
    hidden_1_layer = {'weights':tf.Variable(tf.random_normal([7,n_nodes_hl1])),
                        'biases':tf.Variable(tf.random_normal([n_nodes_hl1]))}

    hidden_2_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1,n_nodes_hl2])),
                        'biases':tf.Variable(tf.random_normal([n_nodes_hl2]))}

    hidden_3_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2,n_nodes_hl3])),
                        'biases':tf.Variable(tf.random_normal([n_nodes_hl3]))}

    hidden_output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl3,n_classes])),
                        'biases':tf.Variable(tf.random_normal([n_classes]))}       


    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']),hidden_1_layer['biases'])
    l1 = tf.nn.relu(l1)

    l2= tf.add(tf.matmul(l1, hidden_2_layer['weights']),hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']),hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, hidden_output_layer['weights'])+hidden_output_layer['biases']
    
    return output

def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_sum(tf.square(prediction - y))
    #cost = tf.nn.tanh(prediction)
    #                       learning rate = 0.001
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    #ressourcen intensiv // durchgänge feed forward + back prop
    hm_epochs = 5

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer(), feed_dict={x: input_data, y: input_data_result})

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for _ in range(int(len(input_data)/batch_size)):
                epoch_x, epoch_y = input_data.train.next_batch(batch_size)
                _, c = sess.run([optimizer,cost], feed_dict={x: epoch_x, y: epoch_y})
                # tf weiß dass die weights angepasst werden mussen
                epoch_loss += c

                print('Epoch',epoch,'complete out of ',hm_epochs, ' loss: ',epoch_loss)

        corr = tf.equal(prediction, y)
        accuracy = tf.subtract(prediction,y)
        #print(corr)
        #print('accuracy', accuracy.eval({x: input_data, y: input_data_result}))
        print(prediction)
        print("\r\n")
        print(y)

#useless?


def main():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = '../Bittrex Extract/brain_out.csv'
    #rel_path = 'test_data.csv'
    abs_file_path = os.path.join(script_dir, rel_path)

    readCSVFile(abs_file_path)

if __name__ == "__main__":
    main()
