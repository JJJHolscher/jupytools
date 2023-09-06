from IPython.display import HTML, Markdown, display

def show_md(string):
    display(Markdown(string))


def show_html(string):
    display(HTML(string))


def show_search_result(result):
    md = ""
    for res in result:
        md += f"#### {res['title']}\n" 
        md += res["snippet"] + res ["link"] + "\n"
    show_md(md)

