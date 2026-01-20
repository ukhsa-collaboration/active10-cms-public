from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# base types
string_schema = openapi.Schema(type=openapi.TYPE_STRING)
integer_schema = openapi.Schema(type=openapi.TYPE_INTEGER)

# model objects
about_schema = openapi.Schema(type=openapi.TYPE_OBJECT, properties={"text": string_schema})
app = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": integer_schema,
        "name": string_schema,
        "description": string_schema,
        "ios": string_schema,
        "android": string_schema,
        "icon": string_schema,
    },
)
apps_schema = openapi.Items(type=openapi.TYPE_ARRAY, items=app)

main_response = openapi.Response(
    "Data for About One You screen",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"about": about_schema, "apps": apps_schema},
    ),
)


def about_on_you_doc():
    return swagger_auto_schema(
        responses={"200": main_response}, operation_description="About One You screen"
    )
