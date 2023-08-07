import modules.scripts as scripts
import gradio as gr
import os

from modules import images, script_callbacks
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state

def on_after_component(component, **kwargs):
    if (component.label == "isTweetCheckbox"):
        gr.Markdown("Hello")

script_callbacks.on_after_component(on_after_component)

def test(isTweet):
    if isTweet:
        return "ツイートします"
    else:
        return "ツイートしません"

class ExtensionTemplateScript(scripts.Script):
    def title(self):
        return "auto-tweet"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion('auto-tweet', open=False):
            with gr.Column():
                isTweet = gr.Checkbox(
                    False,
                    label="isTweetCheckbox"
                )
                button = gr.Button("Test")
                text = gr.Text("Hello")
            button.click(test, inputs=isTweet, outputs=text)
            return [isTweet]
    
    def run(self, p, isTweet):
        proc = process_images(p)
        return proc
