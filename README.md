# Requirements
Tensorflow and Flask need to be installed.

# Instructions
 1. Change the model and label paths in rocketmodels/model.py to match the desired models to run.
 2. Run the app by running:
`python /path/to/repository/rocketmodels/app.py`
 3. There are several parameters that can be passed - the important ones are `port` (by default 5000), `input_layer` (by default `input`) and ``output_layer` (by default `InceptionV3/Predictions/Reshape_1`):
```
usage: app.py [-h] [--input_height INPUT_HEIGHT] [--input_width INPUT_WIDTH]
              [--input_mean INPUT_MEAN] [--input_std INPUT_STD]
              [--input_layer INPUT_LAYER] [--output_layer OUTPUT_LAYER]
              [--port PORT]

optional arguments:
  -h, --help            show this help message and exit
  --input_height INPUT_HEIGHT
                        input height
  --input_width INPUT_WIDTH
                        input width
  --input_mean INPUT_MEAN
                        input mean
  --input_std INPUT_STD
                        input std
  --input_layer INPUT_LAYER
                        name of input layer
  --output_layer OUTPUT_LAYER
                        name of output layer
  --port PORT           port to use

```
