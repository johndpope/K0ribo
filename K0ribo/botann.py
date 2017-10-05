import tensorflow as tf
import tempfile
import pandas as pd

#grund spalten

minutes = tf.feature_column.numeric_column("minutes")
price = tf.feature_column.numeric_column("price")
transactions_amount = tf.feature_column.numeric_column("trans_amount")
coin_amount = tf.feature_column.numeric_column("coin_amount")
past_small = tf.feature_column.numeric_column("change_sm")
past_medium = tf.feature_column.numeric_column("change_md")
past_large = tf.feature_column.numeric_column("change_lg")

base_columns = [minutes, price, transactions_amount, coin_amount, past_small,past_medium,past_large]

#deep_columns = [minutes, price, transactions_amount, coin_amount, past_small,past_medium,past_large]

model_dir = tempfile.mkdtemp()
m = tf.estimator.DNNClassifier(
    model_dir=model_dir,
    linear_feature_columns=base_columns,
    dnn_feature_columns=base_columns,
    dnn_hidden_units=[100,50]
    )

CSV_COLUMNS = ["minutes","price","trans_amount","coin_amount","change_sm","change_md","change_lg"]

def input_fn(data_file, num_epochs, shuffle):
  """Input builder function."""
  df_data = pd.read_csv(
      tf.gfile.Open(data_file),
      names=CSV_COLUMNS,
      skipinitialspace=True,
      engine="python",
      skiprows=1)
      return tf.estimator.inputs.pandas_input_fn(
        x=df_data,
        y=None,
        batch_size=128,
        num_epochs=num_epochs,
        shuffle=shuffle,
        num_threads=5
    )

def train_and_eval(model_dir, model_type, train_steps, train_data, test_data):
    m.train(input_fn=input_fn(train_data, num_epochs=None,shuffle=True ),steps=train_steps)

    results = m.evaluate(input_fn=input_fn(test_data, num_epochs=1, shuffle=False),
    steps=None))

  for key in sorted(results):
    print("%s: %s" % (key, results[key]))

def main(_):
    #Base Directory for output models
    model_dir = ""

    #Valid model types: {'wide', 'deep', 'wide_n_deep'}
    modle_type = "wide_n_deep"

    #Number of training steps
    train_steps = 2000

    #Path to the training data.
    train_data = ""

    #Path to the test data.
    test_data = ""

    train_and_eval(model_dir, model_type, train_steps, train_data, test_data)