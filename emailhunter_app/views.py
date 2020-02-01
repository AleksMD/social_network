from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from emailhunter_app.serializers import EmailVerifySerializer
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
import requests


class EmailVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailVerifySerializer

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if email:
            api_key = settings.EMAILHUNTER_API_KEY
            query_params = f'?email={email}&api_key={api_key}'
            url_to = settings.EMAILHUNTER_URL + query_params
            response = requests.get(url_to)
            data = response.json()
            status_code = response.status_code
            return Response(data,
                            status=status_code,
                            content_type='application/json')
        return Response(status=status.HTTP_400_BAD_REQUEST)
