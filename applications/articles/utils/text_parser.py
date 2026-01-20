import re
from re import compile

from bs4 import BeautifulSoup


def _get_content_type(block_name, style=None):
    if block_name == "a":
        return "link"

    if block_name == "p":
        return "content"

    if block_name == "ol":
        return "numbered_list"

    if block_name == "ul" and style == "list-style-type:square":
        return "white_bullet_list"
    elif block_name == "ul":
        return "bullet_list"

    return "header"


def _retrieve_links(resulting_list, parent):
    content = str(parent)
    soup = BeautifulSoup(content, "html.parser")
    result = False
    links = []

    # find links
    for item in soup.find_all(compile("(a)")):
        if item.name == "a":
            links.append(str(item))
    for link in links:
        content = content.replace(link, "</" + parent.name + ">" + link + "<" + parent.name + ">")

    soup = BeautifulSoup(content, "html.parser")
    for item in soup.find_all(compile("(a|p|h[0-9]{1}|[uo]{1}l)")):
        result = True
        item_plain_text = item.encode().decode("utf-8").replace("&lt;", "<").replace("&gt;", ">")
        item_text = item.get_text().strip()

        # remove first character if the line starts with one of these:
        if item_text.startswith((".", ";", ":")):
            item_text = item_text[1:]

        # skip empty element and single character elements
        if len(item_text) <= 1:
            continue

        resulting_list.append({"type": _get_content_type(item.name), "body": item_plain_text})

    return result


def html_text_to_json(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    resulting_list = []
    for item in soup.find_all(compile("(p|h[0-9]{1}|[uo]{1}l)")):
        soup = BeautifulSoup(str(item), "html.parser")
        links = soup.find_all(compile("(a)"))
        is_list = item.name in ["ul", "ol"]
        style = item.get("style")
        if not links or is_list:
            pattern = r"%(\w+)_(\d+)%"
            view = re.search(pattern, item.get_text())
            if view:
                type_name = view.groups()[0]
                order = view.groups()[1]
                resulting_list.append({"type": type_name.lower(), "order": order})
            else:
                append_element(item, resulting_list)
        else:
            items = (
                re.split("|".join([re.escape(str(it)) for it in links]), str(item))
                if links
                else [item]
            )
            for i in range(len(items) - 1):
                plain_text = (
                    items[i].encode().decode("utf-8").replace("&lt;", "<").replace("&gt;", ">")
                )
                resulting_list.append(
                    {"type": _get_content_type(item.name, style), "body": plain_text}
                )
                append_element(links[i], resulting_list)
            plain_text = (
                items[-1].encode().decode("utf-8").replace("&lt;", "<").replace("&gt;", ">")
            )
            resulting_list.append({"type": _get_content_type(item.name, style), "body": plain_text})
    return resulting_list


def append_element(item, resulting_list):
    style = item.get("style")
    resulting_list.append(
        {
            "type": _get_content_type(item.name, style),
            "body": str(item),
        }
    )
