from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# base types
string_schema = openapi.Schema(type=openapi.TYPE_STRING)
integer_schema = openapi.Schema(type=openapi.TYPE_INTEGER)

# model objects
userinfo_schema = openapi.Schema(type=openapi.TYPE_OBJECT)

lapsed_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "ident": string_schema,
        "copy": string_schema,
        "userinfo": userinfo_schema,
    },
)
onboarding_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "day": integer_schema,
        "copy": string_schema,
        "userinfo": userinfo_schema,
    },
)

main_response = openapi.Response(
    "Data for notifications",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={"onboarding": onboarding_schema, "lapsed": lapsed_schema},
    ),
)


def notifications_doc():
    return swagger_auto_schema(
        responses={"200": main_response}, operation_description="Notifications screen"
    )
