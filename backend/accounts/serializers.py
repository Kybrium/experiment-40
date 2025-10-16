from rest_framework import serializers
from .models import User


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "username", "email", "first_name", "last_name"]

    def create(self, validated_data):
        raise serializers.ValidationError("Creation is not supported for this endpoint.")
    
    def update(self, instance, validated_data):
        raise serializers.ValidationError("Update is not supported for this endpoint.")