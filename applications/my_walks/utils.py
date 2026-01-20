from collections import ChainMap, OrderedDict


def create_target_representation(key, value):
    return OrderedDict([(key, value)])


def create_my_walk_representation(original_representation):
    return OrderedDict(
        [
            (
                "my_walks_dynamic_text",
                create_my_walks_dynamic_text(original_representation),
            ),
            (
                "todays_walks_dynamic_text",
                create_todays_walks_dynamic_text(original_representation),
            ),
        ]
    )


def create_my_walks_dynamic_text(original_representation):
    return OrderedDict(
        [
            (item.get("condition"), item.get("text"))
            for item in original_representation.get("my_walks_dynamic_text")
        ]
    )


def create_todays_walks_dynamic_text(original_representation):
    return OrderedDict(
        [
            (item.get("target_name"), dict(ChainMap(*item.get("target"))))
            for item in original_representation.get("todays_walks_dynamic_text")
        ]
    )
