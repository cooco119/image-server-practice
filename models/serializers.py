from models.models import Users, Image
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    # images = serializers.PrimaryKeyRelatedField(many=True, queryset=Users.objects.all())
    class Meta:
        model = Users
        fields = ('id', 'name')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image_name', 'image_oid', 'user', 'is_private')