def convert(original):
    converted_object = dict()

    converted_object["type"] = "popup"
    converted_object["slug"] = original["slug"]
    converted_object["title"] = original["title"]
    converted_object["properties"] = []

    if original["button"]:
        converted_object["properties"].append({"key": "button", "value": original["button"]})

    if original["noButton"]:
        converted_object["properties"].append({"key": "noButton", "value": original["noButton"]})

    if original["skipButton"]:
        converted_object["properties"].append(
            {"key": "skipButton", "value": original["skipButton"]}
        )

    if original["input_placeholder"]:
        converted_object["properties"].append(
            {"key": "input_placeholder", "value": original["input_placeholder"]}
        )

    if original["text_limit"]:
        converted_object["properties"].append(
            {"key": "text_limit", "value": original["text_limit"]}
        )

    converted_object["media"] = []

    if original["image"]:
        converted_object["media"].append(
            {
                "type": "image",
                "tag": "1",
                "resourceId": "1",
                "label": "first_image",
                "url": original["image"],
            }
        )

    converted_object["children_ids"] = []
    converted_object["article_ids"] = []
    converted_object["description"] = original["message"]
    converted_object["analyticsTag"] = ""

    return converted_object
