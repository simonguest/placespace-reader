# Playspace Reader Concept

This proof of concept uses a quantized [LLaVA](https://llava-vl.github.io/) v1.5 7B model to provide image descriptions of student project output. The goal was to explore whether this approach could help students with vision impairments (i.e., by passing the description to a screenreader).

## Prerequisites

To install the prerequisites, either create and activate a new Conda environment (using environment.yml) or create a new Python virtual env and install the dependencies in requirements.txt.

## Model Download

Download the model files from Huggingface using the `download.sh` script in the models folder.

## Running the App

From the command line, run `gradio app.py`. Once the application is running, open a new browser to `http://127.0.0.1:7860/`

To run the model, first upload an image or click on one of the samples (public gallery projects on Code.org) provided.

You can then ask the model to describe the image, read the text in the image (e.g., a poem), or run a custom prompt. For example, "What color is the font?"

## Limitations

This proof of concept is using a 4bit quantized version of the model, designed to run on commodity hardware, which can sometimes result in inaccurate results. From testing, we've found the model struggles with very small font sizes, fine location placement or directionality (e.g., navigating a maze), and objects it has not been trained on (e.g., Blockly blocks.)

## Additional Screenshots


