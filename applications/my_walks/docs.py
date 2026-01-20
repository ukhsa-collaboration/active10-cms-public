from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# base types
string_schema = openapi.Schema(type=openapi.TYPE_STRING)
integer_schema = openapi.Schema(type=openapi.TYPE_INTEGER)

# model objects
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
