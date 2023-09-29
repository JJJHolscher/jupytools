import codecs
import json
from pathlib import Path

import ipynbname

try:
    IPYNB_PATH = Path(ipynbname.path())
    web_gui = True
except (AttributeError, IndexError):
    web_gui = False


class CellReader:
    def __init__(self):
        self.reset()

    def __call__(self, idx: int):
        """
        Return the content of the previous markdown cell.
        This only works if all pmd calls are in order of occurence.
        """
        i = 0
        for cell in self.cells:
            if cell["cell_type"] == "markdown":
                if i == idx:
                    return "".join(cell["source"])
                i += 1

        self.reset()
        i = 0
        for cell in self.cells:
            if cell["cell_type"] == "markdown":
                if i == idx:
                    return "".join(cell["source"])
                i += 1
        raise IndexError(f"There are only {i} markdown cells but you asked for {idx}.")

    def reset(self):
        f = codecs.open(str(IPYNB_PATH), "r").read()
        f = json.loads(f)
        self.cells = f["cells"]
        return f["cells"]


if web_gui:
    pmd = CellReader()
