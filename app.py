import gradio as gr

def greet(name):
    return "Hello " + name + "!"

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("# Intelligent Complaint Analysis Chatbot")
        name = gr.Textbox(label="Query")
        output = gr.Textbox(label="Response")
        greet_btn = gr.Button("Ask")
        greet_btn.click(fn=greet, inputs=name, outputs=output)

    demo.launch()
