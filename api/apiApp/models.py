# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json

from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

def splitName(email):
	nameSegment = email[:-13]
	arrayName = nameSegment.split("_")
	newArray = []
	for a in arrayName:
		newArray.append(a.title())
	year = "20"+email[-13:-11]+"_"
	name = "_".join(reversed(newArray))
	return year+name+".jpg"


class Player(models.Model):
	email = models.CharField(max_length=200)
	hsClass = models.IntegerField(default=0)
	directoryPath = models.CharField(max_length=200, default="")
	timeTagged = models.DateTimeField('date tagged', default=timezone.now())
	numOfTags = models.IntegerField(default=0)
	aliveStatus = models.BooleanField(default=True)
	user = models.OneToOneField(User, db_index=True, null=True)

	@receiver(post_save, sender=User)
	def create_user_player(sender, instance, created, **kwargs):
	    if created:
	        p = Player.objects.get(email=instance.email)
	        p.user = instance
	        p.save()
	@receiver(post_save, sender=User)
	def save_user_player(sender, instance, **kwargs):
	    pass


	def fancyClass(self):
		clsStr = ""
		for i in range(self.hsClass):
			clsStr += "I"
		if clsStr == "IIII":
			clsStr = "IV"
		return clsStr


	def __str__(self):
		return self.email

	def initPull(self):
		if self.email[-10:] != "milton.edu":
			return "Not valid email"
		else:
			
			self.hsClass = int(self.email[-13:-11])-18	
			self.directoryPath = splitName(self.email)
			# Put in directory pull code
			return "validated"

	def giveName(self):
		nameSegment = self.email[:-13]
		arrayName = nameSegment.split("_")
		newArray = []
		for a in arrayName:
			newArray.append(a.title())
		return " ".join(newArray)


	def jsonify(self):
		return json.dumps({
				"id": self.id,
				"email": self.email,
				"name": self.giveName(),
				"directoryPath": self.directoryPath,
				"timeTagged": self.timeTagged,
				"numOfTags": self.numOfTags,
				"aliveStatus": self.aliveStatus

		},
		sort_keys=True,
 		indent=1,
  		cls=DjangoJSONEncoder)	

  	def dictify(self):
		return {
				"name": self.giveName(),
				"hsClass": self.hsClass,
				"directoryPath": self.directoryPath,
				"timeTagged": self.timeTagged,
				"numOfTags": self.numOfTags,
				"aliveStatus": self.aliveStatus

		}

class TargetRel(models.Model):
	tagger = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='relForward')
	target = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='relBackward')
	latitude = models.FloatField(default=0)
	longitude = models.FloatField(default=0)
	aliveStatus = models.BooleanField(default=True)

	def __str__(self):
		return self.tagger.email + " --> " + self.target.email

	def returnTagInfo(self):
		# This is a simple tag info returner that is going to give me a 2d array 1 hot array
    	# The first array is taggger, postion 1 = class 1 etc
    	# Second array is target
		breakDown = [[0,alrig0,0,0],[0,0,0,0]]
		breakDown[0][self.tagger.hsClass-1] += 1
		breakDown[1][self.target.hsClass-1] += 1
		return breakDown

	def jsonify(self):
		return json.dumps({
				"tagger_id": self.tagger.id,
				"target_id": self.target.id,
				"aliveStatus": self.aliveStatus

		},
		sort_keys=True,
 		indent=1,
  		cls=DjangoJSONEncoder)

  	def giveLatLong(self):
  		return str(self.latitude)+","+str(self.longitude)




