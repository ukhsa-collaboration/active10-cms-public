from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# base types
string_schema = openapi.Schema(type=openapi.TYPE_STRING)
integer_schema = openapi.Schema(type=openapi.TYPE_INTEGER)

# model objects
app_schema = openapi.Schema(type=openapi.TYPE_OBJECT)

link_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "url": string_schema,
        "link": string_schema,
    },
)

terms_conditions_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "latest_version": string_schema,
        "title": string_schema,
        "text": string_schema,
        "button": string_schema,
        "agree": string_schema,
        "links": link_schema,
    },
)

main_response = openapi.Response(
    "Global Rules",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"terms_conditions": terms_conditions_schema, "app": app_schema},
    ),
)


def notifications_doc():
    return swagger_auto_schema(
        responses={"200": main_response}, operation_description="Global Rules"
    )
