from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# base types
string_schema = openapi.Schema(type=openapi.TYPE_STRING)
integer_schema = openapi.Schema(type=openapi.TYPE_INTEGER)

# --- v1 -----------------------------------------------------------------------
# v1: each condition maps to a bare text string.
target_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "condition_0": string_schema,
        "condition_1": string_schema,
        "condition_2": string_schema,
    },
)
my_walks_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "condition_0": string_schema,
        "condition_1": string_schema,
        "condition_2": string_schema,
    },
)
todays_walks_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "target_0": target_schema,
        "target_1": target_schema,
        "target_3": target_schema,
    },
)

main_response = openapi.Response(
    "Data for My walk screen",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "my_walks_dynamic_text": my_walks_schema,
            "todays_walks_dynamic_text": todays_walks_schema,
        },
    ),
)


def my_walk_doc():
    return swagger_auto_schema(
        responses={"200": main_response}, operation_description="My walk screen"
    )


# --- v2 -----------------------------------------------------------------------
# v2: dynamic texts are returned as flat arrays of objects, each carrying both the
# walking text and the wheeling (wheelchair) variant, so the frontend can pick the
# one for its journey.
my_walk_item_schema_v2 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "condition": string_schema,
        "text": string_schema,
        "wheelchair_text": string_schema,
    }
)
target_item_schema_v2 = my_walk_item_schema_v2
today_walk_item_schema_v2 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "target_name": string_schema,
        "target": openapi.Schema(type=openapi.TYPE_ARRAY, items=target_item_schema_v2),
    }
)
my_walks_schema_v2 = openapi.Schema(type=openapi.TYPE_ARRAY, items=my_walk_item_schema_v2)
todays_walks_schema_v2 = openapi.Schema(type=openapi.TYPE_ARRAY, items=today_walk_item_schema_v2)

main_response_v2 = openapi.Response(
    "Data for My walk screen (with wheeling text variants)",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"my_walks_dynamic_text": my_walks_schema_v2, "todays_walks_dynamic_text": todays_walks_schema_v2}
    )
)


def my_walk_doc_v2():
    return swagger_auto_schema(
        responses={"200": main_response_v2},
        operation_description="My walk screen (walking + wheeling text variants)"
    )
