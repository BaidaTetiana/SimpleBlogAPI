### -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from trovero.tasks import update_users_campaigns_insights
import coreapi

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

	def json_commands(file):
		commands = list()
	    for line in open(file, mode="r"):
	        commands.append(json.loads(line))

	def handle(self, *args, **options):
