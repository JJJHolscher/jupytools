from .ipy import web_gui
from IPython.display import HTML, Markdown, display

def show_md(string):
    if web_gui:
        display(Markdown(string))
    else:
        print(string)


def show_html(string):
    display(HTML(string))


def show_search_result(result):
    md = ""
    for res in result:
        md += f"#### {res['title']}\n" 
        md += res["snippet"] + res ["link"] + "\n"
    show_md(md)

