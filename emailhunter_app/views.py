from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from emailhunter_app.serializers import EmailVerifySerializer
from django.http import HttpResponseRedirect
from sn_network import settings
from rest_framework import status
from rest_framework.response import Response


class EmailVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmailVerifySerializer

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        if email:
            api_key = settings.EMAILHUNTER_API_KEY
            query_params = f'?email={email}&api_key={api_key}'
            url_to = settings.EMAILHUNTER_URL + query_params
            return HttpResponseRedirect(redirect_to=url_to)
        return Response(status.HTTP_400_BAD_REQUEST)
