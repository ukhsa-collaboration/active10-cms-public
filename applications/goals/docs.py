from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import GoalSerializers

parameter = openapi.Parameter(
    name="user",
    in_=openapi.IN_QUERY,
    type=openapi.TYPE_STRING,
    description="unique device id\nexample: 00040000-00000000-00RRXXXX-XXZZZZZZ",
)


def goals_doc():
    return swagger_auto_schema(
        responses={"200": GoalSerializers(many=True)},
        manual_parameters=[parameter],
        operation_description="Get list of users goals... first six goals are base.\n"
        "If you execute endpoint without query parameter, it returns base goal only",
    )
