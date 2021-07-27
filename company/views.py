from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import permissions
from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework import generics, permissions
from os import stat
from django.core import mail
from django.shortcuts import render
from rest_framework import generics, permissions, serializers, status
from .models import Document, Company, User
from .serializer import DocumentSerializer, CompanySerializer, UserSerializer, ChangePasswordSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from .emails import sendEmail
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# Create your views here.


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def perform_create(self, serializer):

        serializer.save(company=self.request.user.company)

        # sendEmail()


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAdminUser]


class CompanyDocumentList(generics.GenericAPIView):
    queryset = Company.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        documents = Document.objects.filter(company=pk)
        serializers = DocumentSerializer(documents, many=True)

        return Response(serializers.data)


class UserList(generics.ListCreateAPIView):
    # This grabs all users in the database.
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # This will grab a specific user whith the ID as PK in the URL
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class UserInfo(generics.ListCreateAPIView):
    # This grabs the user's info for the 'logged in user' Token is required to be sent.
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(username=user)


class UserCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            newuser = user_serializer.save()
            if newuser:
                return Response(status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyUserList(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        users = User.objects.filter(company=pk)
        serializers = UserSerializer(users, many=True)

        return Response(serializers.data)


class UpdatePassword(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer_class = ChangePasswordSerializer(data=request.data)

        if serializer_class.is_valid():
            # Check old password
            old_password = serializer_class.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer_class.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)


# Register API

class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
