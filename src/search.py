from copy import copy
from pathlib import Path

import wikipedia
from serpapi import GoogleScholarSearch, GoogleSearch, YoutubeSearch

from .visualize import show_search_result

SERPAPI_KEY = (Path.home() / ".secret/serpapi.key").read_text().strip()
SERPAPI_QUERY = {"hl": "en", "gl": "us", "api_key": SERPAPI_KEY}


def google(query, show=True):
    query_dict = copy(SERPAPI_QUERY)
    query_dict["q"] = query
    result = GoogleSearch(query_dict)
    result = parse_search_result(result)
    if show:
        show_search_result(result)
    return result


def scholar(query, show=True):
    query_dict = copy(SERPAPI_QUERY)
    query_dict["q"] = query
    result = GoogleScholarSearch(query_dict)
    result = parse_search_result(result)
    if show:
        show_search_result(result)
    return result


def youtube(query, show=True):
    query_dict = copy(SERPAPI_QUERY)
    query_dict["search_query"] = query
    result = YoutubeSearch(query_dict)
    result = parse_search_result(result)
    if show:
        show_search_result(result)
    return result


def wiki(query, show=True):
    result = []
    for entry in wikipedia.search(query):
        try:
            page = wikipedia.page(entry, auto_suggest=False)
            summary = page.content[:page.content.find(".")]
            result.append(
                {
                    "title": entry,
                    "snippet": summary,
                    "link": "",
                    "page": page,
                }
            )
        except wikipedia.DisambiguationError:
            pass
    if show:
        show_search_result(result)
    return result


def parse_search_result(result):
    result = result.get_dict()
    out = []
    for entry in result["organic_results"]:
        out.append(
            {
                "title": entry["title"],
                "snippet": entry["snippet"],
                "link": entry["link"],
            }
        )
    return out
