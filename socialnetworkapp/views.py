# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Max
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import *

class UserList(APIView):
	"""
	List all users with details, or create a new user.
	"""
	permission_classes = (permissions.AllowAny,)
	def get(self, request, format=None):
		users = User.objects.all()
		post_info = Post.objects.all()\
				.values('user_id')\
				.aggregate(
					max_post=Max('id'),
					max_likes=Max('likes')
				)

		data = {
			'number_of_users': len(users),
			'max_post_per_user': post_info.get('max_post', 0),
			'max_likes_per_user': post_info.get('max_likes', 0)
		}
		return Response(data)

	def post(self, request, format=None):
		serialized = UserSerializerWithToken(data=request.data)
		if serialized.is_valid():
			serialized.save()
			return Response(serialized.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class PostList(APIView):
	"""
	List all posts, or create a new post.
	"""
	permission_classes = (permissions.IsAuthenticated,)
	def get(self, request, format=None):
		posts = Post.objects.all()
		serializer = PostSerializer(posts, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
	"""
	Retrieve, update or delete a post instance.
	"""
	permission_classes = (permissions.IsAuthenticated,)
	def get_object(self, pk):
		try:
			return Post.objects.get(pk=pk)
		except Post.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		post = self.get_object(pk)
		serializer = PostSerializer(post)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		post = self.get_object(pk)	
		data = dict(request.data)
		serializer = PostSerializer(post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		post = self.get_object(pk)
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)