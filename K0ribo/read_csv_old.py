import tensorflow as tf


'''
0 = akt_Zeit                            [0,1440]
1 = akt Preis                           [0,1]
2 = transaktionen_letzten_5_min         [0,10000]
3 = veränderung letzte 5 min            [-1,2]
4 = veränderung letzte 15 min           [-1,500]
5 = veränderung letzte 30 min           [-1,1000]
6 = Preis in t+30                       [0,1]
'''
depth = 2
filename = "./brain_out.csv"

# filename_queue = tf.train.string_input_producer(
#    ["./brain_out.csv"])


def read_from_csv(filename_queue):
    reader = tf.TextLineReader()
    key, value = reader.read(filename_queue)

    # Default werte, falls eine spalte leer ist
    record_defaults = [[1], [1], [1], [1], [1], [1], [1]]
    col0, col1, col2, col3, col4, col5, col6 = tf.decode_csv(
        value, record_defaults=record_defaults)
    features = tf.stack([col0, col1, col2, col3, col4, col5])
    labels = tf.one_hot(tf.stack([col6]), depth)

    return features, labels


def input_pipeline(batch_size=30, num_epochs=None):
    filename_queue = tf.train.string_input_producer(
        [filename], num_epochs=num_epochs, shuffle=True)
    features, label = read_from_csv(filename_queue)

    min_after_dequeue = 10000
    capacity = min_after_dequeue + 3 * batch_size
    feature_batch, label_batch = tf.train.shuffle_batch(
        [features, label], batch_size=batch_size, capacity=capacity, min_after_dequeue=min_after_dequeue)

    return feature_batch, label_batch


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


'''
file_length = file_len(filename)
features, label = input_pipeline(
    filename=filename, batch_size=file_length, num_epochs=1)
'''
with tf.Session() as sess:
    tf.global_variables_initializer().run()

    file_length = file_len(filename)
    features, label = input_pipeline(batch_size=file_length, num_epochs=1)

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    try:
        print("Label: ", label)
        print("features: ",features)
    except tf.errors.OutOfRangeError:
        print("Done training, epoch reached")
    finally:
        coord.request_stop()

    # coord.join(threads)
