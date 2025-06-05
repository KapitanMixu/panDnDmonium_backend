from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

from dj_rest_auth.views import LoginView
from rest_framework.response import Response

class CustomLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()
        data = original_response.data
        data['user']['role'] = self.user.role
        return Response(data)