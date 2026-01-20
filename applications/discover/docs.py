from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# base types
string_schema = openapi.Schema(type=openapi.TYPE_STRING)
integer_schema = openapi.Schema(type=openapi.TYPE_INTEGER)

# model objects
about_schema = openapi.Schema(type=openapi.TYPE_OBJECT, properties={"text": string_schema})

splash_screen = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": integer_schema,
        "title": string_schema,
        "text": string_schema,
        "button": string_schema,
        "link": string_schema,
    },
)
name_type = openapi.Schema(type=openapi.TYPE_STRING, enum=["image", "image_url", "text"])
discover = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": integer_schema,
        "splash_screen": splash_screen,
        "name_type": name_type,
        "name_text": string_schema,
        "name_image_url": string_schema,
        "name_image": string_schema,
        "description": string_schema,
        "action": string_schema,
        "colour": string_schema,
        "border_colour": string_schema,
        "list_order": integer_schema,
    },
)
cta = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"id": integer_schema, "button": string_schema, "link": string_schema},
)
tip = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": integer_schema,
        "cta": cta,
        "title": string_schema,
        "message": string_schema,
        "fulltext": string_schema,
        "image": string_schema,
        "list_order": integer_schema,
    },
)

discover_schema = openapi.Items(type=openapi.TYPE_ARRAY, items=discover)
tips_schema = openapi.Items(type=openapi.TYPE_ARRAY, items=tip)

main_response = openapi.Response(
    "Discover screen",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"discover": discover_schema, "tips": tips_schema},
    ),
)


def discover_doc():
    return swagger_auto_schema(
        responses={"200": main_response}, operation_description="Discover screen"
    )
