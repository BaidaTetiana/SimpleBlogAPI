from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from socialnetworkapp.models import Post


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):
	token = serializers.SerializerMethodField()
	password = serializers.CharField(write_only=True)

	def get_token(self, obj):
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

		payload = jwt_payload_handler(obj)
		token = jwt_encode_handler(payload)
		return token

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance

	def login(self, user):
		payload = jwt_payload_handler(user)
		token = jwt.encode(payload, settings.SECRET_KEY)
		user_details = {}
		user_details['name'] = "%s %s" % (
			user.first_name, user.last_name)
		user_details['token'] = token

		return user_details

	class Meta:
		model = User
		fields = ('token', 'username', 'email', 'password',)

class PostSerializer(serializers.ModelSerializer):

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Post` instance, given the validated data.
		"""
		instance.likes = instance.likes + int(validated_data.get('likes', '0'))

		instance.save()
		return instance

	class Meta:
		model = Post
		fields = ('name', 'full_text', 'user_id', 'likes')