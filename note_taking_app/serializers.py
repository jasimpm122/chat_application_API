from rest_framework import serializers
from .models import User, Note, History


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'content', 'user', 'created_at', 'modified_at']


class HistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    modified_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = History
        fields = ['modified_at', 'user', 'content']
