import modules.scripts as scripts
import gradio as gr

from modules import script_callbacks, errors
from modules.scripts import PostprocessImageArgs
from modules.shared import opts, OptionInfo

from tweepy import Client


class ExtensionTemplateScript(scripts.Script):
    def __init__(self) -> None:
        super().__init__()
        self.autoTweet = False

    def show(self, _):
        return scripts.AlwaysVisible

    def ui(self, _):
        autoTweetCheckbox = gr.Checkbox(False, label="Enable auto tweet")
        autoTweetCheckbox.change(
            self.onChangeCheckbox, inputs=autoTweetCheckbox, outputs=autoTweetCheckbox
        )

    def before_process(self, _):
        self.resetClient()

    def postprocess_image(self, p, pp: PostprocessImageArgs, *args):
        if self.autoTweet:
            self.client.create_tweet(text="Hello Twitter!")
        return super().postprocess_image(p, pp, *args)

    def onChangeCheckbox(self, value):
        try:
            if value:
                self.resetClient()
            self.autoTweet = value
            return value
        except:
            errors.report("Please auto-tweet set up.")
            return False

    def resetClient(self):
        data = opts.data
        self.client = Client(
            data["bearer_token"],
            data["consumer_key"],
            data["consumer_secret"],
            data["access_token"],
            data["access_token_secret"],
        )


def on_ui_settings():
    section = ("auto tweet", "Auto Tweet")
    settings = [
        ("bearer_token", "Bearer Token"),
        ("consumer_key", "Consumer Key"),
        ("consumer_secret", "Consumer Secret"),
        ("access_token", "Access Token"),
        ("access_token_secret", "Access Token Secret"),
    ]
    for setting in settings:
        opts.add_option(
            setting[0],
            OptionInfo(
                label=setting[1],
                component=gr.Text,
                component_args={"type": "password"},
                section=section,
            ),
        )


script_callbacks.on_ui_settings(on_ui_settings)
