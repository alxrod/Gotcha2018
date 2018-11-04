# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import timezone


class Player(models.Model):
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	hsClass = models.IntegerField(default=0)
	directoryPath = models.CharField(max_length=200, default='')
	timeTagged = models.DateTimeField('date tagged', default=timezone.now())
	numOfTags = models.IntegerField(default=0)
	aliveStatus = models.BooleanField(default=True)

	def __str__(self):
		return self.email

	def initPull(self):
		if self.email[-10:] != 'milton.edu':
			return 'Not valid email'
		else:

			self.hsClass = int(self.email[-13:-11]) - 18
			self.directoryPath = 'fake/file/path'
			# Put in directory pull code
			return 'validated'

	def jsonify(self):
		return json.dumps({
			'id': self.id,
			'email': self.email,
			'directoryPath': self.directoryPath,
			'timeTagged': self.timeTagged,
			'numOfTags': self.numOfTags,
			'aliveStatus': self.aliveStatus

		},
			sort_keys=True,
			indent=1,
			cls=DjangoJSONEncoder)


class TargetRel(models.Model):
	tagger = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='relForward')
	target = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='relBackward')
	aliveStatus = models.BooleanField(default=True)

	def __str__(self):
		return self.tagger.email + ' --> ' + self.target.email

	def returnTagInfo(self):
		# This is a simple tag info returner that is going to give me a 2d array 1 hot array
		# The first array is taggger, postion 1 = class 1 etc
		# Second array is target
		breakDown = [[0, 0, 0, 0], [0, 0, 0, 0]]
		breakDown[0][self.tagger.hsClass - 1] += 1
		breakDown[1][self.target.hsClass - 1] += 1
		return breakDown

	def jsonify(self):
		return json.dumps({
			'tagger_id': self.tagger.id,
			'target_id': self.target.id,
			'aliveStatus': self.aliveStatus

		},
			sort_keys=True,
			indent=1,
			cls=DjangoJSONEncoder)
