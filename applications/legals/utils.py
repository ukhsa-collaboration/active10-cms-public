from re import compile

from bs4 import BeautifulSoup


def _get_block_type(block_name):
    if block_name == "p":
        return "content"

    return "header"


# Alpha version - really simplistic at the moment.
# TODO: Add some useful cool features
def rich_text_to_json(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    resulting_list = []

    for item in soup.find_all(compile("(p|h[0-9]{1}|[uo]{1}l)")):
        resulting_list.append(
            {
                "type": _get_block_type(item.name),
                "body": str(item),
            }
        )

    return resulting_list
