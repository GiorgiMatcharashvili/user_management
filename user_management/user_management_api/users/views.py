from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class UserRegistrationAPIView(APIView):
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAuthenticationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailsAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class UserPermissionsAPIView(APIView):
    def post(self, request, pk):
        user = User.objects.filter(pk=pk).first()
        if user:
            permission_name = request.data.get('permission')
            if permission_name:
                try:
                    content_type = ContentType.objects.get_for_model(User)
                    permission = Permission.objects.get(content_type=content_type, codename=permission_name)
                    user.user_permissions.add(permission)
                    return Response({'message': f'Permission {permission_name} assigned successfully'}, status=status.HTTP_200_OK)
                except:
                    return Response({'message': f'Permission {permission_name} can not be assigned.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Permission name not provided in the request'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)