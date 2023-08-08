import modules.scripts as scripts
import gradio as gr

from modules import script_callbacks, errors
from modules.shared import opts, OptionInfo

from tweepy import OAuthHandler, API, Client, Unauthorized

autoTweet = False


def onChangeCheckbox(value):
    global autoTweet
    autoTweet = value


class AutoTweetScript(scripts.Script):
    def show(self, _):
        return scripts.AlwaysVisible

    def ui(self, _):
        autoTweetCheckbox = gr.Checkbox(False, label="Enable auto tweet")
        autoTweetCheckbox.change(onChangeCheckbox, inputs=autoTweetCheckbox)


def on_image_saved(imageSaveParams: script_callbacks.ImageSaveParams):
    global autoTweet
    if autoTweet == False:
        return
    data = opts.data
    try:
        auth = OAuthHandler(
            data["consumer_key"],
            data["consumer_secret"],
            data["access_token"],
            data["access_token_secret"],
        )
        client = Client(
            data["bearer_token"],
            data["consumer_key"],
            data["consumer_secret"],
            data["access_token"],
            data["access_token_secret"],
        )
        api = API(auth)
        media = api.media_upload(imageSaveParams.filename)
        client.create_tweet(media_ids=[media.media_id])
    except (KeyError, Unauthorized):
        errors.report("Please autp-tweet set up.")


script_callbacks.on_image_saved(on_image_saved)


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
