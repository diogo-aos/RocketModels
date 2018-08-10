import tensorflow as tf
import numpy as np
import os

model_dir = '/rocketmodels/models'
num_top_predictions = 5


def create_graph(model_fn):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(os.path.join(
            model_dir, model_fn), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(image, model):
    """Runs inference on an image.
    Args:
    image: Image file name.
    Returns:
    Nothing
    """
    if not tf.gfile.Exists(image):
        tf.logging.fatal('File does not exist %s', image)
    image_data = tf.gfile.FastGFile(image, 'rb').read()

    image_process = tf.image.decode_and_crop_jpeg(image_data, [0, 0, 299, 299])
    # Start a new session to show example output.
    with tf.Session() as sess:
    # Get an image tensor and print its value.
        image_ary = sess.run([image_process])

    # Creates graph from saved GraphDef.
    create_graph(model)

    with tf.Session() as sess:
        # Some useful tensors:
        # 'softmax:0': A tensor containing the normalized prediction across
        #   1000 labels.
        # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
        #   float description of the image.
        # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
        #   encoding of the image.
        # Runs the softmax tensor by feeding the image_data as input to the graph.
        #         softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, {'Placeholder:0': image_ary})

        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-num_top_predictions:][::-1]
    return top_k

def run_all_models(image):
    models = ['output_graphfirstmodel.pb',
              'output_graphsecondmodel.pb',
              'output_graphthirdmodel.pb',
              'output_graphfourthmodel.pb']
    results = {}
    for m in models:
        predictions = run_inference_on_image(image, m)
        results[m] = list(predictions)

    return results
