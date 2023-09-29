import json
from pathlib import Path
from hashlib import sha256

import openai
from jo3util.root import root_file
import requests
from PIL import Image

from .visualize import show_md

openai.api_key = (Path.home() / ".secret/gpt.key").read_text().strip()

MAIN = root_file()
ROOT = MAIN.parent
GPT_PATH = ROOT / "res" / "gpt" / MAIN.stem
DALLE_PATH = ROOT / "res" / "dall-e" / MAIN.stem


def hash_string(string):
    return sha256(string.encode('utf-8'),
                  usedforsecurity=False).hexdigest()


# See https://platform.openai.com/docs/api-reference/chat/create?lang=python
def gpt(msg, history=None, title=None, show=True):
    """Return a (cached) reply from gpt and the conversation history."""
    if history is None:
        history = []
    elif type(history) is str:
        history = [{"role": "system", "content": history}]
    history.append({"role": "user", "content": msg})

    if not title:
        dump = json.dumps(history, sort_keys=True)
        title = hash_string(dump)

    # Return a cached response if it exists.
    path = GPT_PATH / f"{title}.json"
    if path.exists():
        history = json.loads(path.read_text())
        reply = history[-1]["content"]
        show_md(reply) if show else None
        return reply, history

    elif not path.parent.exists():
        path.parent.mkdir(parents=True)

    reply = (
        openai.ChatCompletion.create(model="gpt-4", messages=history)
        .choices[0]
        .message.content
    )
    history.append({"role": "assistant", "content": reply})

    path.write_text(json.dumps(history))
    show_md(reply) if show else None
    return reply, history


def dalle(prompt, title=None, n=1, size="256x256"):
    assert n == 1

    title = title if title else hash_string(prompt)
    path = DALLE_PATH / f"{title}.png"
    if path.exists():
        return Image.open(path)
    elif not path.parent.exists():
        path.parent.mkdir(parents=True)

    url = openai.Image.create(prompt=prompt, n=n, size=size)["data"][0]["url"]
    image = requests.get(url)
    path.write_bytes(image.content)
    return Image.open(path)
