from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


# 🌍 PUBLIC REGISTER
class PublicRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    phone = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": validated_data["full_name"],
                "phone": validated_data["phone"],
                "role": "public"
            }
        )

        if not created:
            profile.full_name = validated_data["full_name"]
            profile.phone = validated_data["phone"]
            profile.role = "public"
            profile.save()

        return user


# 👑 ADMIN → CREATE (ONLY Judge / School Admin)
class AdminCreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    phone = serializers.CharField()
    role = serializers.ChoiceField(choices=["school_admin", "judge"])

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": validated_data["full_name"],
                "phone": validated_data["phone"],
                "role": validated_data["role"],
            }
        )

        if not created:
            profile.full_name = validated_data["full_name"]
            profile.phone = validated_data["phone"]
            profile.role = validated_data["role"]
            profile.save()

        return user


# 🏫 SCHOOL ADMIN → CREATE Teacher / Student
class SchoolAdminCreateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    phone = serializers.CharField(required=False)
    role = serializers.ChoiceField(choices=["teacher", "student"])

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": validated_data["full_name"],
                "phone": validated_data.get("phone", ""),
                "role": validated_data["role"],
            }
        )

        if not created:
            profile.full_name = validated_data["full_name"]
            profile.phone = validated_data.get("phone", "")
            profile.role = validated_data["role"]
            profile.save()

        return user


# 👤 PROFILE VIEW
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Profile
        fields = [
            "username",
            "full_name",
            "role",
            "phone",
            "email_verified",
            "is_active",
        ]
class SchoolAdminUserListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "full_name",
            "role",
            "phone",
        ]