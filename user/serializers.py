from rest_framework import serializers
from user.models import UserProfile, generate_profile_picture_path
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage

from datetime import date

UserModel = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "profile_picture", "gender", "birthdate"]

    def update(self, instance, validated_data):
        """
        Overrides update method of ModelSerializer. If 'profile_picture' is provided in 'validated_data',
        deletes the current profile picture from the server and replaces it with the provided one.
        """
        profile_picture = validated_data.pop('profile_picture', None)

        if profile_picture:
            if instance.profile_picture and default_storage.exists(instance.profile_picture.path):
                default_storage.delete(instance.profile_picture.path)  # Deletes existing profile picture on server

            new_path = generate_profile_picture_path(instance, profile_picture.name)
            default_storage.save(new_path, profile_picture)  # Stores new image on Server
            instance.profile_picture = new_path  # Stores new image path in model

        instance = super().update(instance, validated_data)
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for User model with nested UserProfile.
    """
    user_profile = UserProfileSerializer(required=True)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 'password2', 'user_profile')
        extra_kwargs = {'password': {'write_only': True, "required": False},
                        'password2': {'write_only': True, "required": False}}

    def create(self, validated_data):
        """
        Creates a UserModel instance and associated UserProfile instance using the validated data.
        """
        validated_data.pop('password2')
        password = validated_data.pop('password')

        user_profile_data = validated_data.pop("user_profile")
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        user_profile_serializer = self.fields['user_profile']
        user_profile_data['user'] = user
        user_profile_serializer.create(user_profile_data)

        return user

    def update(self, instance, validated_data):
        """
         Updates a UserModel instance and its associated UserProfile instance using the validated data.

        """
        user_profile_data = validated_data.pop('user_profile')
        user_profile = instance.user_profile
        user_profile_serializer = self.fields['user_profile']
        user_profile_serializer.update(user_profile, user_profile_data)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()

        return instance

    def validate(self, data):
        """
        Validates the data for password and password2 fields. They must be the same.
        """
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError("The passwords have to be the same.")
        return data

    def validate_password(self, value):
        """
        Validates the send password.
        Raises an Error if the password is less than 6 characters long.
        Raises an Error if no password was sent and the user does not exist yet, which means he is registering.
        """
        if value is not None:
            if len(value) < 6:
                raise serializers.ValidationError("Password must have 8 or more characters.")
        elif self.instance is None:
            raise serializers.ValidationError("This field is required for registering.")

        return value

    def validate_birthdate(self, birthdate: date):
        """
        Check that the birthdate is not in the future.

        """
        if birthdate > date.today():
            raise serializers.ValidationError("Birthdate can't be in the future.")
        return birthdate
