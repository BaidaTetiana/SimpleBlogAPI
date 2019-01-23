### -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

import urllib3

import json

class Command(BaseCommand):
	help = 'automated bot activity'
	args = ''

	SIGNUP = 'signup'
	LOGIN = 'login'
	CREATE = 'posts_create'
	LIKE = 'post_like'
	UNLIKE = 'post_unlike'

	def add_arguments(self, parser):
		pass

	def json_commands(self, file):
		commands = list()
		for line in open(file, mode="r"):
			commands.append(json.loads(line))

	def handle(self, *args, **options):
		http = urllib3.PoolManager()
		data = {'username': 'tetiana','password': '123456'}
		encoded_data = json.dumps(data).encode('utf-8')
		print type(encoded_data)

		r = http.request(
			'POST',
			'http://127.0.0.1:8000/token/login/',
			body=encoded_data,
			headers={
				'Content-Type': 'application/json'
			}
		)

		print json.loads(r.data.decode('utf-8'))