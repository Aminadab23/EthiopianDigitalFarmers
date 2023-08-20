from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out.'})
        except Exception as e:
            return Response({'error': 'Invalid token.'}, status=400)
    else:
        return Response({'error': 'Refresh token not provided.'}, status=400)

from userside.serializers import UserSerializer
from userside.models import User 
from rest_framework import status
@api_view(['PUT'])
def update_user_profile(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
urlpatterns = [
    
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', logout, name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path("user/<str:email>/profile", update_user_profile),
    path('', include("userside.urls")),
    ]+  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)


