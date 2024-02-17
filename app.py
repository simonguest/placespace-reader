import os
import gradio as gr
from PIL import Image
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

example_projects = [
    "space-poetry.png",
    "valentines-poetry.png",
    "neemo-gamelab.png",
    "astronaut-gamelab.png",
    "maze01.png",
    "maze02.png",
]

chat_handler = Llava15ChatHandler(clip_model_path="./models/mmproj-model-f16.gguf")
llm = Llama(
    model_path="./models/ggml-model-q4_k.gguf",
    chat_handler=chat_handler,
    n_ctx=2048,
    logits_all=True,
    n_gpu_layers=-1,
    temperature=0.1,
)


def get_examples():
    return [
        [os.path.join(os.path.dirname(__file__), "projects", x)]
        for x in example_projects
    ]


def generate(image_array, prompt):
    TEMP_FILEPATH = os.path.join(os.path.dirname(__file__), "temp.png")
    # Save the numpy.ndarray image to a png
    image = Image.fromarray(image_array)
    image.save(TEMP_FILEPATH)
    # Generate the description
    output = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant who perfectly describes images.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"file://{TEMP_FILEPATH}"},
                    },
                    {"type": "text", "text": prompt},
                ],
            },
        ]
    )
    print(output)
    return output["choices"][0]["message"]["content"]


def generate_text(image_array):
    return generate(image_array, "Only read the text in this image.")


def generate_description(image_array):
    return generate(
        image_array, "Briefly describe the non-text elements in this image."
    )


with gr.Blocks() as demo:
    gr.Markdown("## Playspace Reader Prototype")
    with gr.Row():
        with gr.Column(scale=1):
            image_selector = gr.Image()
            examples = gr.Examples(examples=get_examples(), inputs=[image_selector])
        with gr.Column(scale=4):
            chatbot = gr.Markdown("Output will appear here")
            describe_button = gr.Button("Describe Image")
            describe_button.click(
                fn=generate_description, inputs=[image_selector], outputs=chatbot
            )
            read_text_button = gr.Button("Read Text in Image")
            read_text_button.click(
                fn=generate_text, inputs=[image_selector], outputs=chatbot
            )
            prompt = gr.Textbox(lines=2, label="Prompt")
            custom_prommpt_button = gr.Button("Run Custom Prompt")
            custom_prommpt_button.click(
                fn=generate, inputs=[image_selector, prompt], outputs=chatbot
            )

demo.launch()
