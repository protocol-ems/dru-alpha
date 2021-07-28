from django.db.models.query import QuerySet
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import serializers
from .models import Company, Document, User
from django.contrib.auth.password_validation import validate_password


class DocumentSerializer(serializers.ModelSerializer):

    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Document
        fields = ['id', 'company', 'documentType',
                  'documentName', 'documentDetails', 'modified', ]

    def create(self, validated_data):
        """
        Create and return a new `Document` instance, given the validated data.
        """
        return Document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Document` instance, given the validated data.
        """
        instance.documentName = validated_data.get(
            'documentName', instance.documentName)
        instance.documentDetails = validated_data.get(
            'documentDetails', instance.documentDetails)
        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):

    documents = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Document.objects.all())

    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())

    class Meta:
        model = Company
        fields = ['id', 'joined', 'name', 'documents', 'users', 'is_active',
                  'main_email', 'ap_email', 'phone', 'street_address', 'zipcode', 'state', 'city']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'company', 'employeeType',
                  'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
