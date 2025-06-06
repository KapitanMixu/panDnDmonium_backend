from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def get_response_data(self, user):
        data = super().get_response_data(user)
        if 'user' not in data:
            data['user'] = {}
        data['user']['role'] = user.role
        return data

from dj_rest_auth.views import LoginView
from rest_framework.response import Response

class CustomLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()
        data = original_response.data
        data['user']['role'] = self.user.role
        return Response(data)