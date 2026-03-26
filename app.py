import gradio as gr
from src.driver import run, word_search

run()

def search(word):
    return word_search(word, show_context=False, max_ctx=0)

with gr.Blocks(theme=gr.themes.Base(), fill_height=True) as demo:
    gr.Markdown(
        "<h1 style='text-align:center;'>Romeo & Juliet — Word Search</h1>"
    )

    with gr.Column(elem_id="main-wrap"):
        # top input section
        with gr.Column(elem_id="input-wrap"):
            word_input = gr.Textbox(
                label="Enter a word",
                placeholder="e.g. love",
                lines=1
            )
            with gr.Row():
                clear_btn = gr.Button("Clear")
                submit_btn = gr.Button("Submit", variant="primary")

        # bottom output section
        output = gr.Markdown(label="Result", elem_id="output-wrap")

    submit_btn.click(search, inputs=word_input, outputs=output)
    word_input.submit(search, inputs=word_input, outputs=output)
    clear_btn.click(lambda: ("", ""), outputs=[word_input, output])

    gr.HTML("""
    <style>
        html, body, .gradio-container {
            height: 100%;
            margin: 0;
        }

        .gradio-container {
            display: flex;
            flex-direction: column;
        }

        #main-wrap {
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
            min-height: calc(100vh - 80px);
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
            gap: 24px;
        }

        #input-wrap {
            width: 100%;
            max-width: 900px;
            margin-top: 10px;
        }

        #output-wrap {
            width: 100%;
            min-height: 300px;
            padding: 20px;
            border-radius: 12px;
            box-sizing: border-box;
        }
    </style>
    """)

if __name__ == "__main__":
    demo.launch(inbrowser=True)