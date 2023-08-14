import modules.scripts as scripts
import gradio as gr

from modules import script_callbacks, errors
from modules.shared import opts, OptionInfo

from tweepy import OAuthHandler, API, Client, Unauthorized, TooManyRequests
from requests.models import Response

autoTweet = False
api: API
auth: OAuthHandler
client: Client


def onChangeCheckbox(value):
    global autoTweet
    autoTweet = value
    if autoTweet:
        global api, auth, client
        data = opts.data
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


class AutoTweetScript(scripts.Script):
    def show(self, _):
        return scripts.AlwaysVisible

    def ui(self, _):
        autoTweetCheckbox = gr.Checkbox(False, label="Enable auto tweet")
        autoTweetCheckbox.change(onChangeCheckbox, inputs=autoTweetCheckbox)


def on_image_saved(imageSaveParams: script_callbacks.ImageSaveParams):
    global autoTweet, selected_imgae
    selected_imgae = None
    if autoTweet == False or "grid" in imageSaveParams.filename:
        return
    global api, auth, client
    try:
        media = api.media_upload(imageSaveParams.filename)
        client.create_tweet(media_ids=[media.media_id])
    except (KeyError, Unauthorized):
        errors.report("Please auto-tweet set up.", exc_info=True)
    except TooManyRequests as e:
        response: Response = e.response
        print(response.headers)
        errors.report("Request limit has been reached.", exc_info=True)


script_callbacks.on_image_saved(on_image_saved)


# 選択中の画像
selected_imgae = None


def on_after_component(component, **_):
    if component.elem_id is None:
        return

    if component.elem_id == "txt2img_gallery":

        def on_select(gallery, evt: gr.SelectData):
            global selected_imgae
            selected_imgae = gallery[evt.index]

        component.select(on_select, inputs=[component])

        with gr.Row():
            tweet_btn = gr.Button(
                "tweet",
            )

        def on_click():
            global selected_imgae
            print(selected_imgae)

        tweet_btn.click(on_click)


script_callbacks.on_after_component(on_after_component)


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
