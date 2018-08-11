from __future__ import print_function
import os

import tensorflow as tf
import numpy as np



num_top_predictions = 5

def preprocess(file_name,
               input_height=299,
               input_width=299,
               input_mean=0,
               input_std=255):
    input_name = 'file_reader'
    file_reader = tf.read_file(file_name, input_name)
    if file_name.endswith(".png"):
        image_reader = tf.image.decode_png(file_reader, channels=3, name="png_reader")
    elif file_name.endswith(".gif"):
        image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name="gif_reader"))
    elif file_name.endswith(".bmp"):
        image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
    else:
        image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    with tf.Session() as sess:
        result = sess.run(normalized)
    return result

def create_graph(model_fn):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(model_fn, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(image_data, model, input_layer, output_layer):
    """Runs inference on an image.
    Args:
    image: Image file name.
    Returns:
    Nothing
    """

    # Creates graph from saved GraphDef.
    create_graph(model)

    with tf.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name(output_layer) # 'final_result:0'

        predictions = sess.run(softmax_tensor, {input_layer: image_data})  # 'Placeholder:0'

        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-num_top_predictions:][::-1]
    return top_k

def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

def run_all_models(image, args):
    model_files = ['/rocketmodels/models/output_graphfirstmodel.pb',
                   '/rocketmodels/models/output_graphsecondmodel.pb',
                   '/rocketmodels/models/output_graphthirdmodel.pb',
                   '/rocketmodels/models/output_graphfourthmodel.pb']
    label_files = ['/rocketmodels/models/output_labelsfirstmodel.txt',
                   '/rocketmodels/models/output_labelssecondmodel.txt',
                   '/rocketmodels/models/output_labelsthirdmodel.txt',
                   '/rocketmodels/models/output_labelsfourthmodel.txt']

    results = {}

    # load image once for all models
    image_data = preprocess(image,
                            args.input_height,
                            args.input_width,
                            args.input_mean,
                            args.input_std)
    
    for m_fn, l_fn in zip(model_files, label_files):
        print('running model {}'.format(m_fn))
        labels = load_labels(l_fn)
        predictions = run_inference_on_image(image_data, m_fn, args.input_layer, args.output_layer)
        results[m_fn] = [labels[l] for l in list(predictions)]

    return results
