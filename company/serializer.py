
from rest_framework import serializers
from rest_framework.fields import ChoiceField
from .models import Company, Document, User, DocumentHeader
from django.contrib.auth.password_validation import validate_password


class DocumentSerializer(serializers.ModelSerializer):

    company = serializers.ReadOnlyField(source='company.name')

    class Meta:
        model = Document
        fields = ['id', 'company', 'document_type',
                  'document_name', 'documentDetails', 'modified', 'table_data', 'flow_data']

    def create(self, validated_data):
        """
        Create and return a new `Document` instance, given the validated data.
        """
        return Document.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Document` instance, given the validated data.
        """
        instance.document_name = validated_data.get(
            'document_name', instance.document_name)
        instance.documentDetails = validated_data.get(
            'documentDetails', instance.documentDetails)
        instance.table_data = validated_data.get(
            'table_data', instance.table_data)
        instance.flow_data = validated_data.get(
            'flow_data', instance.flow_data)

        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):

    documents = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Document.objects.all())

    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())

    document_headers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=DocumentHeader.objects.all())

    class Meta:
        model = Company
        fields = ['id', 'joined', 'name', 'documents', 'users', 'is_active',
                  'phone', 'street_address', 'zipcode', 'state', 'city', 'requested_users', 'document_headers']


class UserSerializer(serializers.ModelSerializer):

    # employee_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'company', 'employee_type',
                  'username', 'email', 'password', 'first_name', 'last_name', 'requested_company']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    # def get_employee_type(self, obj):
    #     return obj.get_employee_type_display()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class DocumentHeaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentHeader
        fields = ['id', 'document_type',
                  'document_detail_name', 'company', 'position']

    def create(self, validated_data):
        return DocumentHeader.objects.create(**validated_data)
