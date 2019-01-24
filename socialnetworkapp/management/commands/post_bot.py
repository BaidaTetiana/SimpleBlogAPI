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
	CREATE = 'post_create'
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
		server = 'http://127.0.0.1:8000'
		auth_token = ''
		file = os.path.join(os.path.dirname(__file__), 'bot_file.json')
		for command in self.json_commands(file):
			headers = {
				'Content-Type': 'application/json',
			}
			if auth_token:
				headers.update({
					'Authorization' : 'Bearer %s' % auth_token
				})
			r = http.request(
				command.get(command.keys()[0], {}).get('method', 'GET'),
				'%s%s' % (server, command.get(command.keys()[0], {}).get('url', '/')),
				body = json.dumps(command.get(command.keys()[0], {}).get('params', {})).encode('utf-8'),
				headers=headers
			)
			auth_token = json.loads(r.data.decode('utf-8')).get('token', auth_token)
			if command.get(INFO, None) is not None:
				print r.data