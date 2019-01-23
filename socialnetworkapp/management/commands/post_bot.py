### -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError

import os
import urllib3
import json

class Command(BaseCommand):
	help = 'automated bot activity'
	args = ''

	INFO = 'info'
	SIGNUP = 'signup'
	LOGIN = 'login'
	CREATE = 'posts_create'
	LIKE = 'post_like'
	UNLIKE = 'post_unlike'

	def add_arguments(self, parser):
		pass

	def json_commands(self, file):
		commands = list()
		for line in open(file, mode='r'):
			commands.append(json.loads(line))
		return commands

	def handle(self, *args, **options):
		http = urllib3.PoolManager()
		file = os.path.join(os.path.dirname(__file__), 'bot_file.json')
		auth_token = ''

		for command in self.json_commands(file):
			if command.get(Command.INFO, None) is not None:
				r = http.request(
					'GET',
					'http://127.0.0.1:8000/users/',
					headers={
						'Content-Type': 'application/json'
					}
				)
				print r.data
			elif command.get(Command.SIGNUP, None):
				r = http.request(
					'POST',
					'http://127.0.0.1:8000/users/',
					body = json.dumps(command.get(Command.SIGNUP, {})).encode('utf-8'),
					headers={
						'Content-Type': 'application/json'
					}
				)
			elif command.get(Command.LOGIN, None):
				r = http.request(
					'POST',
					'http://127.0.0.1:8000/token/login/',
					body = json.dumps(command.get(Command.LOGIN, {})).encode('utf-8'),
					headers={
						'Content-Type': 'application/json'
					}
				)
				auth_token = json.loads(r.data.decode('utf-8')).get('token', '')
			elif command.get(Command.CREATE, None):
				r = http.request(
					'POST',
					'http://127.0.0.1:8000/posts/',
					body = json.dumps(command.get(Command.CREATE, {})).encode('utf-8'),
					headers={
						'Content-Type': 'application/json',
						'Authorization' : 'Bearer %s' % auth_token
					}
				)
			elif command.get(Command.LIKE, None):
				r = http.request(
					'PUT',
					'http://127.0.0.1:8000/post/%d/' % int(command.get(Command.LIKE, {}).get('id', {})),
					body = json.dumps(command.get(Command.LIKE, {}).get('params', {})).encode('utf-8'),
					headers={
						'Content-Type': 'application/json',
						'Authorization' : 'Bearer %s' % auth_token
					}
				)
			else:
				r = http.request(
					'PUT',
					'http://127.0.0.1:8000/post/%d/' % int(command.get(Command.UNLIKE, {}).get('id', {})),
					body = json.dumps(command.get(Command.UNLIKE, {}).get('params', {})).encode('utf-8'),
					headers={
						'Content-Type': 'application/json',
						'Authorization' : 'Bearer %s' % auth_token
					}
				)