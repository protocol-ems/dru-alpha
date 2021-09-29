import re
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework import generics, permissions, serializers, status
from .models import Document, Company, User, DocumentHeader, DocumentImage
from .serializer import DocumentHeaderSerializer, DocumentSerializer, CompanySerializer, UserSerializer, ChangePasswordSerializer, DocumentImageSerializer
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from django.http import HttpResponse
from .emails import sendEmail
from django.core import mail
from django.shortcuts import render

import boto3
from django.conf import settings
from django.http import Http404

# Create your views here.


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):

        serializer.save(company=self.request.user.company)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


class DocumentHeaderList(generics.ListCreateAPIView):
    queryset = DocumentHeader.objects.all()
    serializer_class = DocumentHeaderSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


class DocumentHeaderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentHeader.objects.all()
    serializer_class = DocumentHeaderSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


class CompanyDocumentHeaderList(generics.GenericAPIView):
    queryset = Company.objects.all()
    serializer_class = DocumentHeaderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        documentHeaders = DocumentHeader.objects.filter(company=pk)
        serializers = DocumentHeaderSerializer(documentHeaders, many=True)

        return Response(serializers.data)


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ActiveCompanyList(generics.ListAPIView):
    queryset = Company.objects.all().filter(is_active__in=[True])
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # This will grab a specific user whith the ID as PK in the URL
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]


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


class CompanyWaitList(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        users = User.objects.filter(requested_company=pk)
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


class ImageViewSet(generics.ListCreateAPIView):
    queryset = DocumentImage.objects.all()
    serializer_class = DocumentImageSerializer

    def post(self, request, *args, **kwargs):
        image = request.data['image']
        document = request.data['document']
        company = request.data['company']

        documentSerialized = Document.objects.get(id=document)
        companySerialized = Company.objects.get(id=company)
        DocumentImage.objects.create(
            image=image, document=documentSerialized, company=companySerialized)
        return HttpResponse({'message': 'Image added'}, status=200)


class DocumentImageDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = DocumentImage.objects.all()
    serializer_class = DocumentImageSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        images = DocumentImage.objects.filter(document=pk)
        serializers = DocumentImageSerializer(
            images, many=True, context={'request': request})
        return Response(serializers.data)


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentImage.objects.all()
    serializer_class = DocumentImageSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        images = DocumentImage.objects.filter(id=pk)
        serializers = DocumentImageSerializer(
            images, many=True, context={'request': request})
        return Response(serializers.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
        # s3 = boto3.client('s3')
        # s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        #                  Key=f"media/{item.file.name}")
