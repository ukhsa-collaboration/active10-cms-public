from json import loads
from os import environ

from django.http import HttpResponseRedirect
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from requests import post
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import VersionsSet


def revert_view(request, id=None):
    try:
        VersionsSet.objects.get(pk=id).revert()
    finally:
        return HttpResponseRedirect("/admin/")  # noqa: B012


@api_view(["POST"])
def check_integrity_token(request):
    service_account_info = loads(environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])

    # Define the scope for the API you are accessing
    scopes = ["https://www.googleapis.com/auth/playintegrity"]
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=scopes
    )

    credentials.refresh(Request())
    bearer_token = credentials.token
    integrity_token = request.data.get("integrityToken")
    api_url = (
        "https://playintegrity.googleapis.com/v1/uk.ac.shef.oak.pheactiveten:decodeIntegrityToken"
    )

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    payload = {"integrityToken": str(integrity_token)}

    response = post(api_url, headers=headers, json=payload)

    return Response(response.json(), status=response.status_code)


class IntegrityTokenView(APIView):
    def post(self, request):
        try:
            service_account_info = loads(environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
        except Exception as e:
            print(f"Failed to load service account credentials: {e!s}")
            return Response(
                {"error": "Missing Google service account credentials"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not service_account_info:
            return Response(
                {"error": "Missing Google service account credentials"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        scopes = ["https://www.googleapis.com/auth/playintegrity"]
        integrity_token = request.data.get("integrityToken")
        if not integrity_token:
            return Response({"error": "Missing integrityToken"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=scopes,
            )
            credentials.refresh(Request())
        except Exception as e:
            return Response(
                {"error": f"Failed to initialize credentials: {e!s}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        api_url = "https://playintegrity.googleapis.com/v1/uk.ac.shef.oak.pheactiveten:decodeIntegrityToken"
        headers = {
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
        }
        payload = {
            "integrityToken": str(integrity_token),
        }

        try:
            response = post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response(
                {"error": f"Failed to decode integrity token: {e!s}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
