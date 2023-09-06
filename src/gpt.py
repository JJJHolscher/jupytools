import json
import sys
from pathlib import Path

import openai
import requests
from PIL import Image

from .visualize import show_md

openai.api_key = (Path.home() / ".secret/gpt.key").read_text().strip()

MAIN = Path(sys.argv[0])
ROOT = Path(sys.argv[0]).parent
GPT_PATH = ROOT / "res" / "gpt" / MAIN.name
DALLE_PATH = ROOT / "res" / "dall-e" / MAIN.name


# See https://platform.openai.com/docs/api-reference/chat/create?lang=python
def gpt(msg, history=[], title=None, show=True):
    """Return a (cached) reply from gpt and whether an api call was made."""
    history.append({"role": "user", "content": msg})

    if not title:
        title = hash(json.dumps(history, sort_keys=True))

    # Return a cached response if it exists.
    path = GPT_PATH / f"{title}.json"
    if path.exists():
        history = json.loads(path.read_text())
        return history[-1]["content"], history, False
    else:
        GPT_PATH.mkdir(parents=True, exist_ok=True)

    reply = (
        openai.ChatCompletion.create(model="gpt-4", messages=history)
        .choices[0]
        .message.content
    )
    history.append({"role": "assistant", "content": reply})

    path.write_text(json.dumps(history))
    if show:
        show_md(reply)
    return reply, history, True


def dalle(prompt, title=None, n=1, size="256x256"):
    assert n == 1

    title = title if title else hash(prompt)
    path = DALLE_PATH / f"{title}.png"
    if path.exists():
        return Image.open(path)

    url = openai.Image.create(prompt=prompt, n=n, size=size)["data"][0]["url"]
    image = requests.get(url)
    DALLE_PATH.mkdir(parents=True, exist_ok=True)
    path.write_bytes(image.content)
    return Image.open(path)
