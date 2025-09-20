from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Permission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True},   # Only staff can set this (see below)
            'is_active': {'read_only': True},  # Only staff can set this (see below)
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        request = self.context.get('request')
        # Only staff can set is_staff or is_active True/False
        if request and request.method == 'POST':
            is_staff = self.initial_data.get('is_staff')
            is_active = self.initial_data.get('is_active')
            if (is_staff is not None or is_active is not None) and (
                not request.user or not request.user.is_authenticated or not request.user.is_staff
            ):
                raise serializers.ValidationError("Only staff users can set staff or active status.")
        return super().validate(attrs)

    def to_internal_value(self, data):
        # Prevent non-staff from setting is_staff or is_active
        request = self.context.get('request')
        if request is None or not request.user.is_authenticated or not request.user.is_staff:
            data = data.copy()
            data.pop('is_staff', None)
            data.pop('is_active', None)
        return super().to_internal_value(data)
    
class UserWithPermissionsSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'is_active', 'is_staff', 'is_superuser', 'permissions'
        ]
        read_only_fields = fields

    def get_permissions(self, obj):
        # Get user-specific permissions
        user_permissions = obj.user_permissions.all()

        # Get group permissions
        group_permissions = Permission.objects.filter(group__user=obj)

        # Combine and remove duplicates
        all_permissions = user_permissions | group_permissions
        return all_permissions.values('id', 'codename', 'name', 'content_type__app_label')