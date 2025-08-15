from rest_framework import serializers
from .models import User

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